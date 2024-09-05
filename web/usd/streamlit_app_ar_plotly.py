import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# Set up Streamlit app
st.title('Live Currency Exchange Rate Monitoring')
st.subheader('EUR and SEK compared to USD')

# Function to load data from SQLite database
def load_data():
    conn = sqlite3.connect('currency_data.db')
    query = "SELECT * FROM currency_rates ORDER BY timestamp"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Set refresh interval (in seconds)
refresh_interval = 60  # Refresh every 60 seconds

# Add auto-refresh to the app
st_autorefresh(interval=refresh_interval * 1000, key="data_refresh")

# Load data
df = load_data()

# Check if data is available
if not df.empty:
    # Convert timestamp to datetime for better Plotly handling
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Create Plotly line chart
    fig = px.line(df, x='timestamp', y=['EUR', 'SEK'], labels={'value': 'Exchange Rate', 'timestamp': 'Time'}, 
                  title="EUR and SEK compared to USD", 
                  color_discrete_map={'EUR': 'blue', 'SEK': 'green'})

    # Display plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)

else:
    st.write("No data available yet.")
