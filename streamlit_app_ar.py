import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import time

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

# Streamlit app main loop
while True:
    # Load data
    df = load_data()

    # Check if data is available
    if not df.empty:
        # Plot the data
        fig, ax = plt.subplots()
        ax.plot(df['timestamp'], df['EUR'], label='EUR to USD', color='blue')
        ax.plot(df['timestamp'], df['SEK'], label='SEK to USD', color='green')
        ax.set_xlabel('Timestamp')
        ax.set_ylabel('Exchange Rate')
        plt.xticks(rotation=45)
        plt.legend()

        # Display plot in Streamlit
        st.pyplot(fig)

    else:
        st.write("No data available yet.")

    # Wait for the specified refresh interval, then rerun the app
    time.sleep(refresh_interval)
    st.experimental_rerun()
