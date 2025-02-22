import pandas as pd
import numpy as np
from scipy import stats

def calculate_statistics(df):
    """
    Calculate basic statistics from the water usage data
    """
    stats = {
        'mean_usage': df['usage'].mean(),
        'median_usage': df['usage'].median(),
        'max_usage': df['usage'].max(),
        'min_usage': df['usage'].min(),
        'total_usage': df['usage'].sum(),
        'std_dev': df['usage'].std()
    }
    
    return stats

def analyze_trends(df):
    """
    Analyze trends in water usage data
    """
    # Calculate daily change
    df['daily_change'] = df['usage'].diff()
    
    # Calculate 7-day moving average
    df['moving_avg'] = df['usage'].rolling(window=7).mean()
    
    # Perform basic trend analysis
    trend_analysis = {}
    
    # Overall trend (simple linear regression)
    x = np.arange(len(df))
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, df['usage'])
    
    trend_analysis['overall_trend'] = 'Increasing' if slope > 0 else 'Decreasing'
    trend_analysis['trend_strength'] = abs(r_value)
    
    # Peak usage days
    peak_days = df.nlargest(3, 'usage')[['date', 'usage']]
    trend_analysis['peak_days'] = peak_days.to_dict('records')
    
    # Format trend analysis for display
    trend_text = f"""
    ### Overall Trend Analysis
    - Overall trend: {trend_analysis['overall_trend']}
    - Trend strength (R-value): {trend_analysis['trend_strength']:.2f}
    
    ### Peak Usage Days
    """
    
    for day in trend_analysis['peak_days']:
        trend_text += f"- {day['date'].strftime('%Y-%m-%d')}: {day['usage']:.2f} gallons\n"
    
    return trend_text
