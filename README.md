# Healthcare Analytics Platform

## Overview
The Healthcare Analytics Platform is a comprehensive system designed to extract, transform, and analyze local health data. It provides tools for data integration, cleaning, and visualization to generate actionable insights. The platform supports advanced predictive analytics and interactive dashboards for informed decision-making in public health.

---

## Features
1. **Data Extraction**
   - Fetch data dynamically using the CDC API.
   - Supports large datasets with batch processing and retry mechanisms.

2. **Data Transformation**
   - Handles missing values and standardizes columns.
   - Adapts to column additions or updates dynamically.

3. **Data Storage**
   - Outputs cleaned datasets in both CSV and Parquet formats for flexibility.
   - Prepares data for integration into visualization tools or databases.

4. **Visualization**
   - Supports Power BI dashboards and Python-based interactive visualizations.
   - Enables trend analysis and key performance metric tracking.

5. **Logging and Metrics**
   - Comprehensive logging system for debugging and monitoring ETL workflows.
   - Detailed extraction metrics for performance evaluation.

---

## Folder Structure
```
Healthcare_Analytics_Platform/
├── data/
│   ├── raw/                    # Raw datasets
│   ├── processed/              # Cleaned datasets
│   └── warehouse/              # Data prepared for analysis
├── etl_pipeline/
│   ├── extract.py              # Script to fetch data via API
│   ├── transform.py            # Data cleaning and normalization
│   └── load.py                 # Load cleaned data into storage
├── analytics/
│   ├── eda.ipynb               # Exploratory Data Analysis notebook
│   ├── predictive_model.py     # Predictive modeling script
│   └── visualizations/         # Generated visualizations
├── dashboards/
│   ├── html/                   # Dash-based interactive visualizations
│   └── powerbi_dashboard.pbix  # Power BI project
├── logs/                       # ETL and analytics logs
├── docs/                       # Documentation
│   ├── README.md               # Project overview
│   ├── architecture_diagram.png # Architecture diagram
│   └── requirements.txt        # Dependencies
├── tests/                      # Unit and integration tests
├── deployment/                 # Deployment scripts (Docker, etc.)
└── .gitignore                  # Files and directories to ignore in Git
```

---

## Prerequisites
- **Python 3.8+**
- Required Python libraries:
  - pandas
  - requests
  - tqdm
  - python-dotenv
  - pyarrow or fastparquet (optional for Parquet support)
- **Power BI** for dashboarding (optional)

Install dependencies:
```bash
pip install -r docs/requirements.txt
```

---

## Getting Started

### 1. Set Up Environment
1. Clone the repository:
   ```bash
   git clone https://github.com/LeoRigasaki/Healthcare-Analytics-Platform.git
   cd Healthcare-Analytics-Platform
   ```

2. Configure the `.env` file for API settings:
   ```env
   CDC_API_URL=https://data.cdc.gov/resource/swc5-untb.csv
   BATCH_SIZE=1000
   ```

### 2. Run ETL Pipeline
- Extract data using the `extract.py` script:
  ```bash
  python etl_pipeline/extract.py
  ```
- Clean and transform data using `transform.py`.
- Save processed data to the `data/processed/` directory.

### 3. Visualize Data
- Load processed data into Power BI or use the Dash application (`app.py`) for visualization.

---

## Logging and Monitoring
- Logs for the ETL process are saved in `logs/etl_logs.log`.
- Extraction metrics include total rows, batches processed, and processing time.

---

## Contribution
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Create a pull request.

---

## License
This project is licensed under the MIT License. See `LICENSE` for details.

---

## Acknowledgments
- [CDC API](https://data.cdc.gov/resource/swc5-untb.csv) for providing the data.
- Python and its community for extensive libraries and tools.

---

