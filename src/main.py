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
            max_date = pd.Timestamp.today().normalize().date()
            today = pd.Timestamp.today().normalize().date()
            date_range = st.date_input(
                "Select Date Range",
                value=(today, today),
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

            if 'actions' not in st.session_state:
                st.session_state.actions = {}

            # Input daily actions
            st.header("Daily Actions")
            min_date = df['date'].min()
            max_date = df['date'].max()
            today = pd.Timestamp.today().normalize().date()
            default_date = today if min_date.date() <= today <= max_date.date() else min_date.date()
            selected_date = st.date_input("Select Date to Log Actions", value=today, min_value=min_date.date(), max_value=today)

            if selected_date not in df['date'].dt.date.values:
                new_row = pd.DataFrame({'date': [pd.Timestamp(selected_date)], 'actions': ['']})
                df = pd.concat([df, new_row], ignore_index=True)

            if selected_date not in st.session_state.actions:
                st.session_state.actions[selected_date] = {'laundry': 0, 'showers': 0, 'dishwashing': 0}

            actions = st.session_state.actions[selected_date]
            laundry = actions.get('laundry', 0)
            showers = actions.get('showers', 0)
            dishwashing = actions.get('dishwashing', 0)

            with st.expander(f"Actions for {selected_date.strftime('%Y-%m-%d')}"):
                laundry = st.number_input(f"Laundry loads on {selected_date.strftime('%Y-%m-%d')}", min_value=0, step=1, key=f"laundry_{selected_date}", value=laundry)
                showers = st.number_input(f"Showers on {selected_date.strftime('%Y-%m-%d')}", min_value=0, step=1, key=f"showers_{selected_date}", value=showers)
                dishwashing = st.number_input(f"Dishwashing loads on {selected_date.strftime('%Y-%m-%d')}", min_value=0, step=1, key=f"dishwashing_{selected_date}", value=dishwashing)
                st.session_state.actions[selected_date] = {'laundry': laundry, 'showers': showers, 'dishwashing': dishwashing}
                df.loc[df['date'].dt.date == selected_date, 'actions'] = f"Laundry: {laundry}, Showers: {showers}, Dishwashing: {dishwashing}"

            # Store data with actions in session state
            st.session_state.data = df

            # Show actions for the latest week
            st.header("Latest Week's Actions")
            today = pd.Timestamp.today().normalize().date()
            latest_week_dates = pd.date_range(end=today, periods=7).normalize()
            latest_week = df[df['date'].dt.normalize().isin(latest_week_dates)]

            for date in latest_week_dates.date:
                print(selected_date, date)
                date_actions = st.session_state.actions.get(date, {'laundry': 0, 'showers': 0, 'dishwashing': 0})
                actions_text = f"Laundry: {date_actions['laundry']}, Showers: {date_actions['showers']}, Dishwashing: {date_actions['dishwashing']}"
                st.write(f"{date.strftime('%Y-%m-%d')}: {actions_text}")

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