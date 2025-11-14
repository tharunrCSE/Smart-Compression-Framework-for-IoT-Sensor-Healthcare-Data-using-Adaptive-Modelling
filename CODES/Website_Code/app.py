import zstandard as zstd
import pandas as pd
import time
import os
import pickle
import io
import tempfile  # -- NEW --
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_file, make_response, after_this_request  # -- UPDATED --

# --- Initialize Flask App ---
app = Flask(__name__)
# -- NEW: A secret key is required for sessions --
app.config['SECRET_KEY'] = 'ADCT' 

# --- LZW Algorithm (Unchanged) ---
def lzw_compress(uncompressed: str) -> list:
    dict_size = 256
    dictionary = {chr(i): i for i in range(dict_size)}
    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = c
    if w:
        result.append(dictionary[w])
    return result

# --- Wrapper Functions (Unchanged) ---
def perform_lzw_compression(csv_data_str: str):
    original_size = len(csv_data_str.encode("utf-8"))
    start_time = time.time()
    compressed_data_list = lzw_compress(csv_data_str)
    compression_time = time.time() - start_time
    compressed_bytes = pickle.dumps(compressed_data_list)
    compressed_size = len(compressed_bytes)
    ratio = original_size / compressed_size if compressed_size > 0 else 0
    stats = {
        "method": "LZW (Existing)",
        "original_size": original_size,
        "compressed_size": compressed_size,
        "time": compression_time,
        "ratio": ratio
    }
    return stats, compressed_bytes

def perform_zstd_compression(csv_data_str: str):
    data_bytes = csv_data_str.encode('utf-8')
    original_size = len(data_bytes)
    compressor = zstd.ZstdCompressor(level=5)
    start_time = time.time()
    compressed_data = compressor.compress(data_bytes)
    compression_time = time.time() - start_time
    compressed_size = len(compressed_data)
    ratio = original_size / compressed_size if compressed_size > 0 else 0
    stats = {
        "method": "Z-Standard (Proposed)",
        "original_size": original_size,
        "compressed_size": compressed_size,
        "time": compression_time,
        "ratio": ratio
    }
    return stats, compressed_data

# --- Flask Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])  # -- UPDATED ROUTE --
def compress_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    original_filename = file.filename
    if original_filename == '':
        return jsonify({"error": "No selected file"}), 400

    algorithm = request.form.get('algorithm')
    if not algorithm:
        return jsonify({"error": "No algorithm specified"}), 400
        
    try:
        csv_data_str = file.read().decode('utf-8')
        
        results_stats = {}
        compressed_data = b""
        file_extension = ""
        
        if algorithm == 'lzw':
            results_stats, compressed_data = perform_lzw_compression(csv_data_str)
            file_extension = "lzw"
        elif algorithm == 'z-standard':
            results_stats, compressed_data = perform_zstd_compression(csv_data_str)
            file_extension = "zst"
        else:
            return jsonify({"error": "Unknown algorithm"}), 400

        base_filename = os.path.splitext(original_filename)[0]
        download_filename = f"{base_filename}.{file_extension}"

        # -- NEW: Save data to a temporary file on the SERVER --
        # 1. Create a temp file. delete=False prevents it from being deleted on close.
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_extension}')
        # 2. Write the compressed data to it
        temp_file.write(compressed_data)
        # 3. Close it
        temp_file.close()
        
        # -- UPDATED: Store the FILE PATH (a small string) in the session --
        session[f'{algorithm}_temp_path'] = temp_file.name  # e.g., '/tmp/tmp123abc.lzw'
        session[f'{algorithm}_filename'] = download_filename

        # Add formatted strings for easy display
        results_stats['ratio_str'] = f"{results_stats['ratio']:.2f}:1"
        results_stats['time_str'] = f"{results_stats['time']:.4f} s"
        
        # Add download info to the JSON response
        results_stats['download_url'] = url_for('download_file', algorithm=algorithm)
        results_stats['download_filename'] = download_filename
        
        return jsonify(results_stats)

    except Exception as e:
        app.logger.error(f"Error during compression: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/download/<string:algorithm>')  # -- UPDATED ROUTE --
def download_file(algorithm):
    """
    Serves the compressed file from the server's temp directory.
    """
    # Retrieve file path and download name from session
    path_key = f'{algorithm}_temp_path'
    name_key = f'{algorithm}_filename'
    
    temp_path = session.pop(path_key, None)
    download_filename = session.pop(name_key, f"compressed.{algorithm}")

    if not temp_path or not os.path.exists(temp_path):
        return "Error: File not found or session expired. Please compress again.", 404

    # -- NEW: Use @after_this_request to delete the file AFTER sending it --
    @after_this_request
    def cleanup_file(response):
        try:
            os.remove(temp_path)
        except OSError as e:
            app.logger.error(f"Error deleting temp file {temp_path}: {e}")
        return response

    # Use send_file to send the data from the server's disk
    return send_file(
        temp_path,
        as_attachment=True,
        download_name=download_filename,
        mimetype='application/octet-stream'
    )

# --- Run the App ---
if __name__ == '__main__':
    app.run(debug=True)