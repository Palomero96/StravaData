import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="Strava Activities Dashboard",
    page_icon="🏃‍♂️",
    layout="wide"
)

st.title("Strava Activities Dashboard")
st.caption("A simple dashboard to visualize your Strava activities.")

# --- Data Loading ---
@st.cache_data
def load_data(file_path):
    """Safely loads data from a CSV file."""
    if os.path.exists(file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            st.error(f"Error loading {os.path.basename(file_path)}: {e}")
            return None
    return None

# Define file paths
run_file = os.path.join('data', 'run.csv')
swim_file = os.path.join('data', 'swim.csv')
bike_file = os.path.join('data', 'bike.csv')

# Load datasets
run_df = load_data(run_file)
swim_df = load_data(swim_file)
bike_df = load_data(bike_file)

# Adjust types
run_df['start_date_local'] = pd.to_datetime(run_df['start_date_local'], errors='coerce')
swim_df['start_date_local'] = pd.to_datetime(swim_df['start_date_local'], errors='coerce')
bike_df['start_date_local'] = pd.to_datetime(bike_df['start_date_local'], errors='coerce')

# Add Columnn Move to strava.py
run_df['activity_type'] = "Run"
swim_df['activity_type'] = "Swim"
bike_df['activity_type'] = "Bike"

df = pd.concat([run_df, swim_df, bike_df], ignore_index=True)

# --- Dashboard Tabs ---
tab_all,tab_run, tab_swim, tab_bike = st.tabs(["📈 All", "🏃‍♂️ Running", "🏊‍♂️ Swimming", "🚴‍♂️ Biking"])

########## TAB ALL ##########
with tab_all:
    st.header("Overall Activity Totals")
    # Data Transformation for metrics
    total_runs = len(run_df) if run_df is not None else 0
    total_swim = len(swim_df) if swim_df is not None else 0
    total_bike = len(bike_df) if bike_df is not None else 0
    total_activities = len(df) if df is not None else 0
    
    df['Year'] = df["start_date_local"].dt.year
    current_year = datetime.now().year
    last_year_total_activities = len(df[df['Year']==current_year-1])
    current_year_total_activities = len(df[df['Year']==current_year])
    # METRICS
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Activities Logged", total_activities)
    col2.metric("Total Activities Logged Last Year", last_year_total_activities)
    col3.metric("Total Activities Logged Current Year", current_year_total_activities)
    # CHART: Activity Count Totals
    activity_counts = pd.DataFrame({
        "Activity Type": ["Run", "Swim", "Bike"],
        "Count": [total_runs, total_swim, total_bike]
    })
    
    # Display the bar chart
    st.subheader("Activity Count Totals")
    st.bar_chart(activity_counts.set_index("Activity Type"))
    
    st.divider()
    # CHART: Activities by month filtered by year
    st.subheader("Activity Count by Month")
    # Unique Years
    available_years = sorted(df['Year'].unique())
    # Create selector to filter with
    selected_year = st.selectbox(
    "Choose year to filter:", 
    available_years
    )
    df_filtered = df[df['Year'] == selected_year].copy()
    # Get Month name
    df_filtered['Month'] = df_filtered['start_date_local'].dt.month_name()
    # Group by month and activity
    df_grouped = df_filtered.groupby(['Month','activity_type']).size().reset_index(name='Count')
    order_months = [
    "January", "February", "March", "April", "May", "June", 
    "July", "August", "September", "October", "November", "December"
    ]
    
    # Create figure
    fig = px.bar(
        df_grouped,
        x='Month',
        y='Count',
        color='activity_type',
        category_orders={"Month": order_months}
    )

    
    st.plotly_chart(fig, use_container_width=True)
    st.divider()
    #Activities by Year
    # Get Month name
    df['Year'] = df['start_date_local'].dt.year
    # Group by month and activity
    df_grouped = df.groupby(['Year','activity_type']).size().reset_index(name='Count')

    # Create figure
    fig_year = px.bar(
        df_grouped,
        x='Year',
        y='Count',
        color='activity_type'
    )

    st.subheader("Activity Count by Year")
    st.plotly_chart(fig_year, use_container_width=True)


########## TAB RUN ##########
with tab_run:

    if run_df is not None:
        # METRICS
        col1, col2, col3 = st.columns(3)
        total_distance = run_df['distance_km'].sum()
        total_runs = len(run_df)
        avg_pace = run_df['pace_min_km'].mean()
        
        col1.metric("Total Runs", f"{total_runs}")
        col2.metric("Total Distance (km)", f"{total_distance:.2f}")
        col3.metric("Average Pace (min/km)", f"{avg_pace:.2f}")
        st.divider()
        #CHART: Distance Evolution
        st.subheader("Distance Evolution")
        run_df_distance = run_df[['start_date_local', 'distance_km']]
        st.line_chart(run_df_distance,
                      x='start_date_local',
                      y='distance_km')
        st.divider()
        #CHART: HeartRate Evolution
        st.subheader("HeartRate Evolution")
        run_df_heart= run_df[['start_date_local', 'average_heartrate']]
        st.line_chart(run_df_heart,
                      x='start_date_local',
                      y='average_heartrate')
        st.divider()
        #CHART: Time Evolution
        st.subheader("Time Evolution")
        run_df_time= run_df[['start_date_local', 'moving_time']]
        st.line_chart(run_df_time,
                      x='start_date_local',
                      y='moving_time')
        st.divider()
        #CHART: Pace Evolution
        st.subheader("Pace Evolution")
        run_df_pace= run_df[['start_date_local', 'pace_min_km']]
        st.line_chart(run_df_pace,
                      x='start_date_local',
                      y='pace_min_km')
        st.divider()
        st.dataframe(run_df)
        
        
    else:
        st.warning(f"Could not find run data at `{run_file}`.")
        st.info("Please run the `strava.py` script first to generate the activity files.")

########## TAB SWIM ##########
with tab_swim:
    if swim_df is not None:
        # METRICS
        col1,col2 = st.columns(2)
        total_swim_activities = len(swim_df)
        total_swim_distance = swim_df['distance'].sum()
        col1.metric("Total Swims", f"{total_swim_activities}")
        col2.metric("Total Distance (m)", f"{total_swim_distance}")
        st.divider()

        #CHART: Distance Evolution
        st.subheader("Distance Evolution")
        swim_df_distance = swim_df[['start_date_local', 'distance']]
        st.line_chart(swim_df_distance,
                      x='start_date_local',
                      y='distance')
        st.divider()
        #CHART: Heart Evolution
        st.subheader("Heart Evolution")
        swim_df_distance = swim_df[['start_date_local', 'average_heartrate']]
        st.line_chart(swim_df_distance,
                      x='start_date_local',
                      y='average_heartrate')
        st.divider()
        #CHART: Elapsed Evolution
        st.subheader("Time Evolution")
        swim_df_distance = swim_df[['start_date_local', 'moving_time']]
        st.line_chart(swim_df_distance,
                      x='start_date_local',
                      y='moving_time')
        st.divider()
        #CHART: Pace Evolution
        st.subheader("Pace Evolution")
        swim_df_distance = swim_df[['start_date_local', 'pace_seconds_100m']]
        st.line_chart(swim_df_distance,
                      x='start_date_local',
                      y='pace_seconds_100m')
        st.divider()
        st.dataframe(swim_df)
    else:
        st.warning(f"Could not find swim data at `{swim_file}`.")

########## TAB BIKE ##########
with tab_bike:
    if bike_df is not None:
        # METRICS
        col1, col2, col3 = st.columns(3)
        total_bike_distance = bike_df['distance'].sum()/100
        total_bike_activities = len(bike_df)
        avg_pace_bike = bike_df['pace_seconds_100m'].mean()
        
        col1.metric("Total Bike Activities", f"{total_bike_activities}")
        col2.metric("Total Distance (km)", f"{total_bike_distance:.2f}")
        col3.metric("Average Pace (min/km)", f"{avg_pace_bike:.2f}")

        #CHART: Distance Evolution
        st.subheader("Distance Evolution")
        bike_df_distance = bike_df[['start_date_local', 'distance']]
        st.line_chart(bike_df_distance,
                    x='start_date_local',
                    y='distance')
        st.divider()

        #CHART: HeartRate Evolution
        st.subheader("Heart Evolution")
        bike_df_heart = bike_df[['start_date_local', 'average_heartrate']]
        st.line_chart(bike_df_heart,
                    x='start_date_local',
                    y='average_heartrate')
        st.divider()

        #CHART: Elapsed Time Evolution
        st.subheader("Time Evolution")
        bike_df_time = bike_df[['start_date_local', 'moving_time']]
        st.line_chart(bike_df_time,
                    x='start_date_local',
                    y='moving_time')
        st.divider()

        #CHART: Pace Evolution
        st.subheader("Pace Evolution")
        bike_df_pace = bike_df[['start_date_local', 'pace_seconds_100m']] 
        st.line_chart(bike_df_pace,
                    x='start_date_local',
                    y='pace_seconds_100m')
        st.divider()

        st.dataframe(bike_df)
    else:
        st.warning(f"Could not find bike data at `{bike_file}`.")
