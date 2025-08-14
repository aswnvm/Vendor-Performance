# Vendor Performance Analytics

Vendor Performance Analytics is a Python-based project designed to analyze and visualize supplier/vendor performance data using both Python scripts and Power BI dashboards.

- **Statistical Analysis**: Includes hypothesis testing, t-tests, p-values, and confidence intervals to validate insights.

## 📂 Project Structure

```bash
./
├── assets
│   ├── bg.png
│   ├── data
│   └── logs
├── main.py
├── notebooks
│   ├── Exploratory Data Analysis.ipynb
│   ├── Vendor Performance Analysis.ipynb
│   └── ingestion_db.ipynb
├── pyproject.toml
├── scripts
│   ├── get_vendor_summary.py
│   └── ingestion_db.py
└── README.md
```

## 🚀 Features

- **Data Analysis**: Jupyter notebooks for exploratory and performance analysis.
- **Database Integration**: Vendor performance data stored in a local SQLite database.
- **Interactive Dashboard**: Power BI report for visual insights.
- **Script Automation**: Python scripts for automated data processing.

## 🛠 Installation & Project Setup

### 1. Install UV

Make sure you have Python 3.10+ installed, then run:

```bash
pip install uv
```

### Verify installation

```bash
uv --version
```

1. **Clone the repository**

```bash

git clone https://github.com/aswnvm/Vendor-Performance.git
cd Vendor-Performance
   ```

2. **Install project packages**

```bash
uv install
```

3. **Activate virtual environment**

```bash
uv venv
```

## 📦 Requirements

- Python 3.10+
- Power BI Desktop (for .pbix file)
- UV dependency manager
- SQLite (bundled with Python)

[**Vendor Performance Dashboard**](https://app.powerbi.com/view?r=eyJrIjoiOGM5MzQ5YzktYzI5Mi00MDk3LWE3NmYtY2Y0YmEwOWNiNmYwIiwidCI6IjBmZGYwYzdmLTA2OWMtNDE0YS05MTM2LWQwZjRlYmIzMDliOSJ9)

[**Download Vendor Data CSV**](https://drive.google.com/file/d/1GwPlIw_FqaRvSgmaUZyPBd6pcsJrbhnQ/view?usp=sharing)
