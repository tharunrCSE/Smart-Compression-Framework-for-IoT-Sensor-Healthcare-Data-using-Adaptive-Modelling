# **README – Smart Compression Framework for IoT Sensor Healthcare Data**

### *Comparative Analysis of LZW (Existing) and Zstandard (Proposed) Compression Techniques*

---

## **Overview**

The rise of IoT-driven healthcare systems has led to continuous real-time monitoring of vital parameters such as heart rate, oxygen saturation, blood pressure, and temperature. Efficient transmission and storage of this data are essential to support:

* Remote patient monitoring
* Predictive analytics
* Emergency alerts
* Low-cost IoT deployment

This project proposes a **Smart Compression Framework** tailored for healthcare sensor data, comparing:

### **Existing Method**

✔ LZW Compression
✔ Traditional dictionary-based technique

### **Proposed Method**

✔ Zstandard (Zstd)
✔ Faster, more efficient modern compression algorithm

Both algorithms are evaluated on the **Human Vital Signs Dataset (Kaggle)** using metrics such as:

* Compression Ratio (CR)
* Space Saving (SS)
* Compression Time
* Decompression Time

A **Flask-based Web Application** is also provided to perform compression interactively.

---

## **Key Features**

✔ Complete implementation of **LZW** and **Zstd**<br>
✔ Comparison notebooks for performance evaluation<br>
✔ Dataset handling + preprocessing<br>
✔ Real-time compression visualization through a web UI<br>
✔ Full project documentation (Abstract Review, Final Report, Review PPTs)<br>
✔ Reproducible code structured in methodology folders

---

## **Project Directory Structure**


```
Smart-Compression-Framework/
│
├── Abstract_Review1.pdf
├── Final_Project_Report.pdf
├── Review 2 Smart_Compression_Framework_for_IoT_Sensor_Data.pptx
├── Review 3 Advanced-Data-Compression-Techniques-Project-Review.pptx
│
└── CODES/
    │
    ├── Existing Methodology/
    │   ├── compressed_data.lzw
    │   ├── compressed_dataset.xz
    │   ├── decompressed_data.csv
    │   ├── human_vital_signs_dataset_2024.csv
    │   ├── LZW_Dataset_Compression.ipynb
    │   ├── LZW_Logic.ipynb
    │   └── .ipynb_checkpoints/
    │       ├── LZMA_Dataset_Compression-checkpoint.ipynb
    │       ├── LZW_Dataset_Compression-checkpoint.ipynb
    │       └── LZW_Logic-checkpoint.ipynb
    │
    ├── Proposed Methodology/
    │   ├── Comparison_lzw_zstd.ipynb
    │   ├── compressed_data.lzw
    │   ├── compressed_dataset.zst
    │   ├── decompressed_data.csv
    │   ├── human_vital_signs_dataset_2024.csv
    │   ├── Logic_ZStd.ipynb
    │   ├── LZW_Dicstonary.ipynb
    │   ├── zstd_Dataset_Compression.ipynb
    │   ├── zstd_hash.ipynb
    │   └── .ipynb_checkpoints/
    │       ├── Comparison_lzma_zstd-checkpoint.ipynb
    │       ├── Comparison_lzw_zstd-checkpoint.ipynb
    │       ├── Logic_ZStd-checkpoint.ipynb
    │       ├── LZW_Dicstonary-checkpoint.ipynb
    │       └── zstd_Dataset_Compression-checkpoint.ipynb
    │
    └── Website_Code/
        ├── app.py
        ├── requirements.txt
        │
        ├── static/
        │   ├── main.js
        │   └── style.css
        │
        └── templates/
            └── index.html
```

---

## **Methodology Overview**

### **1️ LZW (Existing Method)**

* Dictionary-based lossless compression
* Good for repetitive patterns
* Works well on structured sensor datasets
* Slower than modern compression algorithms
* Higher overhead for large files

---

### **2️ Zstandard (Proposed Method)**

* Combines Finite State Entropy (FSE) with Huffman coding
* Very high compression speed
* Extremely fast decompression (ideal for IoT nodes)
* Adjustable compression levels
* Excellent for real-time and streaming applications

---

## **How to Run the Code**

### **1. Navigate to the Website_Code folder**

```
cd CODES/Website_Code
```

### **2. Install dependencies**

```
pip install -r requirements.txt
```

### **3. Run the Web Application**

```
python app.py
```

### **4. Open in browser**

```
http://127.0.0.1:5000/
```

This interface allows users to:

* Upload CSV sensor files
* Compress using LZW or Zstd
* View compression ratios
* Download compressed output

---

## **Dataset Used**

**Human Vital Sign Dataset – Kaggle (2024)**
Contains continuous healthcare signals such as:

* Heart Rate
* Blood Pressure
* Temperature
* SpO₂

Dataset Size: **~38.7 MB**

---

## **Metrics Used**

| Metric                     | Formula                    | Meaning         |
| -------------------------- | -------------------------- | --------------- |
| **Compression Ratio (CR)** | CR = Original / Compressed | Higher = Better |
| **Space Saving (SS)**      | SS = (1 – 1/CR) × 100      | % saved         |
| **Compression Time**       | Processing time            | Lower = Better  |
| **Decompression Time**     | Recovery speed             | Lower = Better  |

---

## **Included Documents**

The root project folder contains:

* ✔ **Abstract Review**
* ✔ **Final Project Report**
* ✔ **Review 2 PPT**
* ✔ **Review 3 PPT**

Useful for documentation, submission, and evaluation.

---

## **Future Works**

* Adaptive compression switching (based on entropy)
* On-device low-memory compression (edge computing)
* Add Brotli, Snappy, LZ4 for extended comparison
* Integrate with MQTT/Node-RED IoT pipeline
* Secure compressed transmission (AES + Zstd)
* Real-time dashboards with Flask + JS

---

## **Team Members**

* **Tharun R (22MIC0061)**
* **Ravishankar G (22MIC0034)**
* **Anirudhan R (22MIC0067)**
* **I Mohamed Israar (22MID0101)**

**Supervisor:**
*Balaji N — Assistant Professor (Sr. Grade 1)*
School of Computer Science and Engineering (SCOPE), VIT Vellore

---

## **Conclusion**

This project demonstrates that **Zstandard (Zstd)** significantly improves performance over **LZW**, offering:

* Higher compression efficiency
* Faster execution
* Better scalability
* Real-time suitability for IoT healthcare systems

The Smart Compression Framework provides a practical, adaptive, and efficient foundation for handling continuous sensor streams in healthcare monitoring environments.

---
