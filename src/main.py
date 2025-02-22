import streamlit as st
import pandas as pd
from utils.data_processor import process_csv_data, validate_data
from utils.visualizations import create_time_series_plot, create_usage_histogram
from utils.analysis import calculate_statistics, analyze_trends
import io

st.set_page_config(
    page_title="Water Usage Analysis Dashboard",
    page_icon="💧",
    layout="wide"
)

def main():
    st.title("💧 Water Usage Analysis Dashboard")

    # Sidebar for data upload and controls
    with st.sidebar:
        st.header("Data Input")
        uploaded_file = st.file_uploader("Upload Water Usage CSV", type=['csv'])

        if 'data' in st.session_state:
            st.header("Date Range Selection")
            min_date = st.session_state.data['date'].min()
            max_date = st.session_state.data['date'].max()
            date_range = st.date_input(
                "Select Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )

    # Main content area
    if uploaded_file is not None:
        try:
            # Process and validate data
            df = process_csv_data(uploaded_file)

            # Store data in session state
            st.session_state.data = df

            # Create three columns for statistics
            col1, col2, col3 = st.columns(3)
            stats = calculate_statistics(df)

            with col1:
                st.metric("Average Daily Usage", f"{stats['mean_usage']:.2f} gal")
            with col2:
                st.metric("Peak Usage", f"{stats['max_usage']:.2f} gal")
            with col3:
                st.metric("Total Usage", f"{stats['total_usage']:.2f} gal")

            # Visualization section
            st.header("Usage Visualization")
            chart_type = st.selectbox(
                "Select Chart Type",
                ["Line Chart", "Bar Chart", "Usage Distribution"]
            )

            if chart_type in ["Line Chart", "Bar Chart"]:
                fig = create_time_series_plot(df, chart_type)
                st.plotly_chart(fig, use_container_width=True)
            else:
                fig = create_usage_histogram(df)
                st.plotly_chart(fig, use_container_width=True)

            # Trend Analysis
            st.header("Trend Analysis")
            trends = analyze_trends(df)
            st.write(trends)

            # Export functionality
            st.header("Export Analysis")
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download Processed Data",
                data=csv,
                file_name="processed_water_usage.csv",
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
    else:
        st.info("Please upload a CSV file to begin analysis")
        st.markdown("""
        ### Expected CSV Format:
        Your CSV should contain the following columns:
        - `Access Code`: Your water meter access code
        - `Time Interval`: Date in MM/DD/YYYY format
        - `Consumption`: Water usage in CCF (will be converted to gallons)
        - `Units`: Should be 'CCF'

        Example:
        ```
        Access Code,Time Interval,Consumption,Units
        12345,02/22/2025,2.5,CCF
        12345,02/23/2025,2.1,CCF
        12345,02/24/2025,2.8,CCF
        ```

        Note: The dashboard automatically converts CCF (Centum Cubic Feet) to gallons
        (1 CCF = 748.052 gallons) for easier understanding.
        """)

if __name__ == "__main__":
    main()