# Predictive Maintenance for Industrial Machinery

This project leverages machine learning to predict equipment failure using sensor data from the NASA Turbofan Engine Degradation dataset. It simulates a complete data pipeline, from raw data ingestion into a SQL database to advanced analytics and visualization.

**Key Features:**
*   **Data Ingestion:** Loads and cleans raw sensor data into an SQLite database.
*   **Feature Engineering:** Creates relevant features for predictive modeling.
*   **Machine Learning:** Employs a Random Forest model to predict equipment failure.
*   **Visualization:** Generates a CSV output for powerful insights in Tableau.

## Technologies Used

*   **Python:** The core programming language for scripting and machine learning.
*   **Pandas:** Essential for efficient data manipulation and feature engineering.
*   **SQLite:** Used to simulate a robust production-grade database.
*   **Scikit-learn:** Provides tools for data scaling, model training, and evaluation.
*   **Tableau:** For creating interactive and insightful data visualizations.

---

## 📂 Project Structure

```
.
├── engine_data.db
├── Maintance Dashboard.twb
├── maintenance_predictions.csv
├── predict_failure.py
├── README.md
├── setup_database.py
└── train_FD001.txt
```

---

## 🛠️ How to Run the Project

### Step 1: Setup

1.  **Download the Data:**
    *   Search for the "NASA Turbofan Engine Degradation dataset".
    *   From the downloaded ZIP file, find and copy `train_FD001.txt` into this project's directory.

2.  **Install Python Libraries:**
    *   Open your terminal in the project directory and run:
    ```bash
    pip install pandas scikit-learn
    ```
    *(Note: `sqlite3` is part of the standard Python library, so no separate installation is needed.)*

### Step 2: Run the Scripts

You must run the scripts in order.

1.  **Run the Data Pipeline:**
    *   This script loads `train_FD001.txt`, cleans it, and saves it to a database file.
    ```bash
    python setup_database.py
    ```
    *   You will see a new file named `engine_data.db` appear in your folder.

2.  **Run the Analytics:**
    *   This script reads from `engine_data.db`, engineers features, trains the model, and saves the predictions.
    ```bash
    python predict_failure.py
    ```
    *   This will print a **Model Performance Report** to your terminal and create the `maintenance_predictions.csv` file.

---

## 📊 Tableau Visualization Guide

Use the generated `maintenance_predictions.csv` file to build your dashboards.

1.  Open Tableau and connect to **"Text File"**.
2.  Select `maintenance_predictions.csv`.
3.  Go to a new worksheet.

### Dashboard 1: Equipment Health Monitoring (EHM)

This dashboard tracks the health of a single engine over its lifespan.

1.  Drag `time_in_cycles` (from the "Measures" panel) to **Columns**.
2.  Drag `sensor_7` and `sensor_7_roll_mean` (from "Measures") to **Rows**.
3.  Tableau will create two line charts. Right-click the axis and select **"Dual Axis"** to overlay them.
4.  Drag `unit_number` (from "Dimensions") to the **Filters** card. Select a single unit (e.g., unit "3") to see its specific trend.

![Equipment Health Monitoring Dashboard](Screenshot%202025-10-28%20at%2010.26.20%E2%80%AFPM.png)

### Dashboard 2: Failure Predictions

This dashboard shows the model's performance.

**Part A: Confusion Matrix (Table)**

1.  Drag `will_fail_soon` (the "actual" value) to **Columns**.
2.  Drag `prediction` (the "predicted" value) to **Rows**.
3.  Drag `Number of Records` to the **Text** card (on the Marks pane).
4.  This creates a table showing True Positives, True Negatives, False Positives, and False Negatives.

**Part B: Prediction Pie Chart**

1.  Create a new sheet.
2.  Drag `prediction` to the **Color** card.
3.  Drag `Number of Records` to the **Angle** card.
4.  Change the Mark type from "Automatic" to **"Pie"**.
5.  Drag `prediction` and `Number of Records` to the **Label** card to see the percentages.
