import pandas as pd
import numpy as np
from datetime import datetime

def process_csv_data(file):
    """
    Process uploaded CSV file into a pandas DataFrame
    """
    df = pd.read_csv(file)
    
    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Sort by date
    df = df.sort_values('date')
    
    # Handle missing values
    df = df.dropna()
    
    return df

def validate_data(df):
    """
    Validate the uploaded data format and content
    """
    required_columns = ['date', 'usage']
    
    # Check for required columns
    if not all(col in df.columns for col in required_columns):
        return {
            'is_valid': False,
            'message': "CSV must contain 'date' and 'usage' columns"
        }
    
    # Check for valid date format
    try:
        pd.to_datetime(df['date'])
    except Exception:
        return {
            'is_valid': False,
            'message': "Invalid date format. Please use YYYY-MM-DD"
        }
    
    # Check for numeric usage values
    if not pd.to_numeric(df['usage'], errors='coerce').notnull().all():
        return {
            'is_valid': False,
            'message': "Usage values must be numeric"
        }
    
    # Check for negative usage values
    if (df['usage'] < 0).any():
        return {
            'is_valid': False,
            'message': "Usage values cannot be negative"
        }
    
    return {
        'is_valid': True,
        'message': "Data validation successful"
    }
