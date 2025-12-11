import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(page_title="Forensic Data Analysis", layout="wide")

# We assume you renamed the file to something simple like 'pm10_data.csv'
FILENAME = 'pm10_data.csv' 
THRESHOLD_PM10 = 45  # WHO Threshold

# ---------------------------------------------------------
# DATA LOADING FUNCTION
# ---------------------------------------------------------
@st.cache_data
def load_data():
    try:
        # Load the CSV
        df = pd.read_csv(FILENAME)
        
        # Rename columns for consistency
        # Adjust these indices if your CSV columns are in a different order
        # Based on your upload, column 0 is value, column 1 is date
        df.columns = ['pm10', 'timestamp']
        
        # Convert timestamp
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values(by='timestamp')
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# ---------------------------------------------------------
# MAIN APP
# ---------------------------------------------------------
st.title("🛡️ Logic Reconstruction: Automated Safety Triggers")

df = load_data()

if not df.empty:
    # 1. METRICS
    hazard_count = len(df[df['pm10'] > THRESHOLD_PM10])
    total_samples = len(df)
    
    col1, col2 = st.columns(2)
    col1.metric("Total Data Points", f"{total_samples:,}")
    col2.metric("Hazard Events Detected", f"{hazard_count:,}", delta_color="inverse")

    # 2. PLOT
    fig = go.Figure()

    # Data Line
    fig.add_trace(go.Scatter(
        x=df['timestamp'], y=df['pm10'],
        mode='lines', name='PM10', line=dict(color='#1f77b4')
    ))

    # Threshold Line
    fig.add_hline(y=THRESHOLD_PM10, line_dash="dash", line_color="red", 
                  annotation_text="Trigger Limit (45)", annotation_position="top right")

    # Red Zone (Hazard)
    fig.add_hrect(y0=THRESHOLD_PM10, y1=df['pm10'].max()*1.1, 
                  fillcolor="red", opacity=0.1, line_width=0,
                  annotation_text="HAZARD STATE (Red LED)", annotation_position="top left")

    # Green Zone (Safe)
    fig.add_hrect(y0=0, y1=THRESHOLD_PM10, 
                  fillcolor="green", opacity=0.05, line_width=0,
                  annotation_text="SAFE STATE (Green LED)", annotation_position="bottom left")

    fig.update_layout(
        title="Digital Reconstruction of Firmware Logic",
        xaxis_title="Time",
        yaxis_title="PM10 (µg/m³)",
        template="plotly_white",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)
