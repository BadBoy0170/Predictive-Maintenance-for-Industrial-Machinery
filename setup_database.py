import pandas as pd
import sqlite3
import os

# --- Configuration ---
DATABASE_NAME = 'engine_data.db'
TABLE_NAME = 'sensor_readings'
DATA_FILE = 'train_FD001.txt' # Make sure this file is in the same directory
# ---

# Define the column names for the dataset
column_names = [
    'unit_number', 'time_in_cycles', 'setting_1', 'setting_2', 'setting_3',
    'sensor_1', 'sensor_2', 'sensor_3', 'sensor_4', 'sensor_5',
    'sensor_6', 'sensor_7', 'sensor_8', 'sensor_9', 'sensor_10',
    'sensor_11', 'sensor_12', 'sensor_13', 'sensor_14', 'sensor_15',
    'sensor_16', 'sensor_17', 'sensor_18', 'sensor_19', 'sensor_20', 'sensor_21'
]

def setup_database():
    """
    Simulates a data pipeline by loading raw sensor data from a text file
    into a structured SQLite database.
    """
    print(f"Starting data pipeline setup...")

    # Check if data file exists
    if not os.path.exists(DATA_FILE):
        print(f"Error: Data file '{DATA_FILE}' not found.")
        print("Please download the 'train_FD001.txt' file from the NASA Turbofan dataset and place it in the same directory.")
        return

    # 1. Load the NASA Turbofan Engine Degradation dataset
    # The file is space-delimited and has no header
    try:
        df = pd.read_csv(DATA_FILE, sep=' ', header=None)
    except Exception as e:
        print(f"Error reading data file: {e}")
        return

    # The dataset has two extra empty columns at the end due to the space delimiter
    # We drop them and assign the correct column names
    df.drop(columns=[26, 27], inplace=True)
    df.columns = column_names

    print(f"Successfully loaded and parsed data with {len(df)} rows.")

    # 2. Create a connection to a new SQLite database file
    # This will create the file if it doesn't exist
    conn = sqlite3.connect(DATABASE_NAME)
    
    # 3. Save the Pandas DataFrame into a new SQL table
    try:
        df.to_sql(TABLE_NAME, conn, if_exists='replace', index=False)
        print(f"Data saved to table '{TABLE_NAME}' in '{DATABASE_NAME}'.")
    except Exception as e:
        print(f"Error saving data to SQL: {e}")
    finally:
        conn.close()

    print(f"---")
    print(f"Database '{DATABASE_NAME}' and table '{TABLE_NAME}' created successfully.")
    print(f"---")

if __name__ == "__main__":
    setup_database()