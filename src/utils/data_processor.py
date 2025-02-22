import pandas as pd
import numpy as np
from datetime import datetime

def ccf_to_gallons(ccf):
    """
    Convert CCF (Centum Cubic Feet) to gallons
    1 CCF = 748.052 gallons
    """
    return ccf * 748.052

def process_csv_data(file):
    """
    Process uploaded CSV file into a pandas DataFrame
    """
    # Read CSV with more lenient whitespace handling and clean column names
    df = pd.read_csv(file, skipinitialspace=True)
    df.columns = [col.lstrip('\ufeff').strip() for col in df.columns]

    # Debug print to show raw column names
    print("DEBUG - Raw CSV columns:", df.columns.tolist())
    print("DEBUG - Column names with repr():")
    for col in df.columns:
        print(f"  {repr(col)}")
    print("DEBUG - Column types:", df.dtypes)

    # Convert date format with more robust error handling
    try:
        df['date'] = pd.to_datetime(df['Time Interval'], format='%m/%d/%Y')
    except ValueError as e:
        raise ValueError(f"Error parsing dates. Please ensure dates are in MM/DD/YYYY format. Error: {str(e)}")

    # Convert consumption from CCF to gallons
    df['usage'] = df['Consumption'].apply(ccf_to_gallons)

    # Select and reorder needed columns
    df = df[['date', 'usage']]

    # Sort by date
    df = df.sort_values('date')

    # Handle missing values
    df = df.dropna()

    return df

def validate_data(df):
    """
    Validate the uploaded data format and content
    """
    required_columns = ['Access Code', 'Time Interval', 'Consumption', 'Units']

    # Print detailed comparison for debugging
    print("\nDEBUG - Validation comparison:")
    print("Required columns:", required_columns)
    print("Actual columns:", list(df.columns))
    print("\nDetailed column comparison:")
    for req_col in required_columns:
        if req_col in df.columns:
            print(f"Found: {req_col}")
        else:
            print(f"Missing: {req_col} (type expected: str, actual columns types: {df.dtypes.to_dict()})")

    # Check for required columns
    missing_cols = [col for col in required_columns if col not in list(df.columns)]
    if missing_cols:
        return {
            'is_valid': False,
            'message': f"CSV must contain these columns: {', '.join(required_columns)}. Missing: {', '.join(missing_cols)}"
        }

    # Check for numeric consumption values
    if not pd.to_numeric(df['Consumption'], errors='coerce').notnull().all():
        return {
            'is_valid': False,
            'message': "Consumption values must be numeric"
        }

    # Check for negative consumption values
    if (pd.to_numeric(df['Consumption']) < 0).any():
        return {
            'is_valid': False,
            'message': "Consumption values cannot be negative"
        }

    # Verify units are CCF
    if not all(unit.strip().upper() == 'CCF' for unit in df['Units']):
        return {
            'is_valid': False,
            'message': "All units must be in CCF"
        }

    return {
        'is_valid': True,
        'message': "Data validation successful"
    }