import os
import pandas as pd

def convert_unrate_excel_to_csv(
    excel_path: str = "data/UNRATE.xlsx", 
    csv_path: str = "data/UNRATE.csv"
):
    """
    Reads the 'Monthly' sheet from FRED UNRATE.xlsx file and exports it to a clean CSV.
    Ensures standard date and unemployment rate columns.
    """
    if not os.path.exists(excel_path):
        raise FileNotFoundError(f"Input file not found: {excel_path}")

    # Load 'Monthly' sheet which contains the actual time series observations
    df = pd.read_excel(excel_path, sheet_name='Monthly')
    
    # Normalize column names: rename observation_date to DATE if preferred or ensure both compatibility
    # Ensure proper datetime format YYYY-MM-DD
    df['DATE'] = pd.to_datetime(df['observation_date']).dt.strftime('%Y-%m-%d')
    df['UNRATE'] = pd.to_numeric(df['UNRATE'], errors='coerce')
    
    # Standard format: DATE, UNRATE (with observation_date also preserved if needed)
    df_clean = df[['DATE', 'UNRATE', 'observation_date']]
    
    df_clean.to_csv(csv_path, index=False)
    print(f"Successfully converted '{excel_path}' to '{csv_path}'")
    print(f"Row count: {len(df_clean)}")
    print("Sample output:")
    print(df_clean.head())

if __name__ == "__main__":
    convert_unrate_excel_to_csv()
