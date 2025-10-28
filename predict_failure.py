import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# --- Configuration ---
DATABASE_NAME = 'engine_data.db'
TABLE_NAME = 'sensor_readings'
OUTPUT_CSV = 'maintenance_predictions.csv'
FAILURE_THRESHOLD = 30 # Number of cycles before failure to predict
KEY_SENSORS = ['sensor_2', 'sensor_3', 'sensor_4', 'sensor_7', 'sensor_11', 'sensor_12', 'sensor_15']
ROLLING_WINDOW_SIZE = 5
# ---

def predict_failures():
    """
    Loads sensor data from the SQL database, engineers features,
    trains a model to predict failures, and saves the results.
    """
    print("Starting predictive maintenance analysis...")
    
    # 1. Data Loading
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        df = pd.read_sql_query(f'SELECT * FROM {TABLE_NAME}', conn)
        conn.close()
        print(f"Successfully loaded {len(df)} records from '{DATABASE_NAME}'.")
    except Exception as e:
        print(f"Error: Could not load data from '{DATABASE_NAME}'.")
        print(f"Did you run 'python setup_database.py' first? Details: {e}")
        return

    # 2. Feature Engineering
    print("Engineering features...")
    
    # Calculate Remaining Useful Life (RUL)
    # Get the max cycle for each unit
    max_cycles = df.groupby('unit_number')['time_in_cycles'].max().reset_index()
    max_cycles.columns = ['unit_number', 'max_cycles']
    # Merge back to get RUL for each row
    df = pd.merge(df, max_cycles, on='unit_number')
    df['rul'] = df['max_cycles'] - df['time_in_cycles']

    # Create Binary Label
    # 1 if failure is imminent (RUL <= 30), 0 otherwise
    df['will_fail_soon'] = df['rul'].apply(lambda x: 1 if x <= FAILURE_THRESHOLD else 0)

    # Create Rolling Features
    rolling_features = []
    for sensor in KEY_SENSORS:
        # Calculate rolling mean
        mean_col_name = f'{sensor}_roll_mean'
        df[mean_col_name] = df.groupby('unit_number')[sensor].rolling(window=ROLLING_WINDOW_SIZE).mean().reset_index(level=0, drop=True)
        rolling_features.append(mean_col_name)
        
        # Calculate rolling std dev
        std_col_name = f'{sensor}_roll_std'
        df[std_col_name] = df.groupby('unit_number')[sensor].rolling(window=ROLLING_WINDOW_SIZE).std().reset_index(level=0, drop=True)
        rolling_features.append(std_col_name)

    # Drop rows with NaN values created by the rolling window
    original_rows = len(df)
    df.dropna(inplace=True)
    print(f"Dropped {original_rows - len(df)} rows with NaN values after rolling feature calculation.")

    # 3. Machine Learning (Random Forest)
    print("Training Random Forest model...")

    # Define features (X) and target (y)
    features = ['time_in_cycles'] + KEY_SENSORS + rolling_features
    target = 'will_fail_soon'

    X = df[features]
    y = df[target]

    # Split the data (shuffling is important)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Initialize and train a RandomForestClassifier
    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train_scaled, y_train)

    # Make predictions on the test set
    y_pred = model.predict(X_test_scaled)

    # Print a classification_report
    print("\n--- Model Performance Report ---")
    print(classification_report(y_test, y_pred, target_names=['Predicted Safe (0)', 'Predicted to Fail (1)']))
    print("---------------------------------\n")

    # 4. Output
    print(f"Saving test results to '{OUTPUT_CSV}'...")
    
    # Create a new DataFrame for the test results
    # We use the original, unscaled test data for easier interpretation in Tableau
    results_df = df.loc[X_test.index].copy()
    results_df['prediction'] = y_pred
    
    # Select key columns for the final CSV
    output_columns = ['unit_number', 'time_in_cycles', 'rul', 'will_fail_soon', 'prediction'] + features
    results_df[output_columns].to_csv(OUTPUT_CSV, index=False)

    print("Analysis complete. Results saved.")

if __name__ == "__main__":
    predict_failures()