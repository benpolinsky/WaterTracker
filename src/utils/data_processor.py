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
    df = pd.read_csv(file)

    # Rename columns to remove spaces and standardize names
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]

    # Convert date format
    df['date'] = pd.to_datetime(df['time_interval'], format='%m/%d/%Y')

    # Convert consumption from CCF to gallons
    df['usage'] = df['consumption'].apply(ccf_to_gallons)

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
    required_columns = ['access_code', 'time_interval', 'consumption', 'units']

    # Check for required columns (case-insensitive)
    df_cols = [col.strip().lower() for col in df.columns]
    if not all(col.lower() in df_cols for col in required_columns):
        return {
            'is_valid': False,
            'message': "CSV must contain 'Access Code', 'Time Interval', 'Consumption', and 'Units' columns"
        }

    # Check for valid date format
    try:
        pd.to_datetime(df['time_interval'], format='%m/%d/%Y')
    except Exception:
        return {
            'is_valid': False,
            'message': "Invalid date format. Please use MM/DD/YYYY format for Time Interval"
        }

    # Check for numeric consumption values
    if not pd.to_numeric(df['consumption'], errors='coerce').notnull().all():
        return {
            'is_valid': False,
            'message': "Consumption values must be numeric"
        }

    # Check for negative consumption values
    if (pd.to_numeric(df['consumption']) < 0).any():
        return {
            'is_valid': False,
            'message': "Consumption values cannot be negative"
        }

    # Verify units are CCF
    if not all(unit.strip().upper() == 'CCF' for unit in df['units']):
        return {
            'is_valid': False,
            'message': "All units must be in CCF"
        }

    return {
        'is_valid': True,
        'message': "Data validation successful"
    }