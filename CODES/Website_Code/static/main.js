// Global object to store results for comparison
const comparisonResults = {
    lzw: null,
    'z-standard': null,
};

// Listen to all form submissions
document.querySelectorAll('.compression-form').forEach(form => {
    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Stop default form submission

        const algorithm = form.dataset.algorithm;
        const resultsDiv = form.querySelector('.results');
        const loaderDiv = form.querySelector('.loader');
        const downloadContainer = form.querySelector('.download-container'); // -- NEW --
        const fileInput = form.querySelector('input[type="file"]');
        
        if (!fileInput.files[0]) {
            alert("Please select a file.");
            return;
        }

        // Show loader and clear old results/links
        resultsDiv.innerHTML = '';
        downloadContainer.innerHTML = ''; // -- NEW --
        loaderDiv.style.display = 'block';

        const formData = new FormData(form);

        try {
            // Send file to Flask backend
            const response = await fetch('/compress', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Compression failed');
            }

            const results = await response.json();

            // Display results in the card
            resultsDiv.innerHTML = `
                <p><strong>Original Size:</strong> ${results.original_size} bytes</p>
                <p><strong>Compressed Size:</strong> ${results.compressed_size} bytes</p>
                <p><strong>Compression Time:</strong> ${results.time_str}</p>
                <p><strong>Compression Ratio:</strong> ${results.ratio_str}</p>
            `;

            // -- NEW: Create and display the download link --
            if (results.download_url && results.download_filename) {
                downloadContainer.innerHTML = `
                    <a href="${results.download_url}" class="download-link" download="${results.download_filename}">
                        Download ${results.download_filename}
                    </a>
                `;
            }

            // Store results and update comparison table
            comparisonResults[algorithm] = results;
            renderComparisonTable();

        } catch (error) {
            resultsDiv.innerHTML = `<p style="color: red;"><strong>Error:</strong> ${error.message}</p>`;
        } finally {
            // Hide loader
            loaderDiv.style.display = 'none';
        }
    });
});

// Renders the main comparison table
function renderComparisonTable() {
    // ... (rest of this function is unchanged)
    const tableContainer = document.getElementById('results-table');
    const lzw = comparisonResults.lzw;
    const zstd = comparisonResults['z-standard'];

    if (!lzw && !zstd) return;

    let tableHTML = `
        <table>
            <thead><tr><th>Algorithm</th><th>Original Size</th><th>Compressed Size</th><th>Compression Time</th><th>Compression Ratio</th></tr></thead>
            <tbody>
    `;
    if (lzw) {
        tableHTML += `<tr>
            <td>${lzw.method}</td>
            <td>${lzw.original_size} bytes</td>
            <td>${lzw.compressed_size} bytes</td>
            <td>${lzw.time_str}</td>
            <td>${lzw.ratio_str}</td>
        </tr>`;
    }
    if (zstd) {
        tableHTML += `<tr>
            <td>${zstd.method}</td>
            <td>${zstd.original_size} bytes</td>
            <td>${zstd.compressed_size} bytes</td>
            <td>${zstd.time_str}</td>
            <td>${zstd.ratio_str}</td>
        </tr>`;
    }
    tableHTML += '</tbody></table>';
    tableContainer.innerHTML = tableHTML;
}

// Handles the "Download CSV" button
function downloadComparisonCSV() {
    // ... (rest of this function is unchanged)
    let csvContent = 'data:text/csv;charset=utf-8,Algorithm,Original Size (bytes),Compressed Size (bytes),Compression Time (s),Compression Ratio\n';
    
    if (comparisonResults.lzw) {
        const lzw = comparisonResults.lzw;
        csvContent += `${lzw.method},${lzw.original_size},${lzw.compressed_size},${lzw.time.toFixed(4)},${lzw.ratio.toFixed(2)}:1\n`;
    }
    if (comparisonResults['z-standard']) {
        const zstd = comparisonResults['z-standard'];
        csvContent += `${zstd.method},${zstd.original_size},${zstd.compressed_size},${zstd.time.toFixed(4)},${zstd.ratio.toFixed(2)}:1\n`;
    }

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', 'compression_comparison.csv');
    document.body.appendChild(link).click();
    document.body.removeChild(link);
}

document.getElementById('download-csv').addEventListener('click', downloadComparisonCSV);