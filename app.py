import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(page_title="Forensic Data Analysis", layout="wide")

# This matches the file you uploaded
FILENAME = 'pm10_values.csv' 
THRESHOLD_PM10 = 45  # WHO Threshold set in your Arduino code

# ---------------------------------------------------------
# DATA LOADING FUNCTION
# ---------------------------------------------------------
@st.cache_data
def load_data():
    try:
        # Load the CSV
        df = pd.read_csv(FILENAME)
        
        # Rename the columns to be simpler to work with
        # Your file has: 'pm10', 'date (Europe/London)'
        df.columns = ['pm10', 'timestamp']
        
        # Convert the timestamp column to proper datetime objects
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Sort by time so the line graph connects points correctly
        df = df.sort_values(by='timestamp')
        
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return pd.DataFrame()

# ---------------------------------------------------------
# MAIN APP INTERFACE
# ---------------------------------------------------------
st.title("🛡️ Logic Reconstruction: Automated Safety Triggers")
st.markdown("""
**Objective:** Verify the microcontroller's safety logic by reconstructing the threshold breaches 
from the uploaded telemetry data.
""")

df = load_data()

if not df.empty:
    # -----------------------------------------------------
    # 1. CALCULATE METRICS (The "Evidence")
    # -----------------------------------------------------
    total_samples = len(df)
    
    # Identify Hazard Events (Where PM10 > 45)
    hazard_events = df[df['pm10'] > THRESHOLD_PM10]
    hazard_count = len(hazard_events)
    
    # Calculate Safety Percentage
    safety_percentage = ((total_samples - hazard_count) / total_samples) * 100

    # Display Metrics at the top
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Data Points", f"{total_samples:,}")
    col2.metric("Hazard Events (LED = RED)", f"{hazard_count:,}", delta_color="inverse")
    col3.metric("Safe Operation Rate", f"{safety_percentage:.
