import streamlit as st
import pandas as pd
import os

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

# --- Dashboard Tabs ---
tab_all,tab_run, tab_swim, tab_bike = st.tabs(["📈 All", "🏃‍♂️ Running", "🏊‍♂️ Swimming", "🚴‍♂️ Biking"])

with tab_all:
    st.header("Overall Activity Totals")

    total_runs = len(run_df) if run_df is not None else 0
    total_swim = len(swim_df) if swim_df is not None else 0
    total_bike = len(bike_df) if bike_df is not None else 0
    total_activities = total_runs + total_swim + total_bike

    # Display total activities as a metric
    st.metric("Total Activities Logged", total_activities)

    # Data for the bar chart
    activity_counts = pd.DataFrame({
        "Activity Type": ["Running", "Swimming", "Biking"],
        "Count": [total_runs, total_swim, total_bike]
    })

    # Display the bar chart
    st.subheader("Activity Count Breakdown")
    st.bar_chart(activity_counts.set_index("Activity Type"))
    
    #Activities by month

    #Activities by year
    


with tab_run:

    if run_df is not None:
        
        col1, col2, col3 = st.columns(3)
        total_distance = run_df['distance_km'].sum()
        total_runs = len(run_df)
        avg_pace = run_df['pace_min_km'].mean()
        
        col1.metric("Total Runs", f"{total_runs}")
        col2.metric("Total Distance (km)", f"{total_distance:.2f}")
        col3.metric("Average Pace (min/km)", f"{avg_pace:.2f}")

        st.dataframe(run_df)
        st.divider()
        
    else:
        st.warning(f"Could not find run data at `{run_file}`.")
        st.info("Please run the `strava.py` script first to generate the activity files.")

with tab_swim:
    if swim_df is not None:
        st.dataframe(swim_df)
    else:
        st.warning(f"Could not find swim data at `{swim_file}`.")

with tab_bike:
    if bike_df is not None:
        st.dataframe(bike_df)
    else:
        st.warning(f"Could not find bike data at `{bike_file}`.")
