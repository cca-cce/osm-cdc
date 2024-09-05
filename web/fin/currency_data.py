import os
import requests
import sqlite3
import time

# Load environment variables from .env file
#from dotenv import load_dotenv
#load_dotenv()
#API_KEY = os.getenv('EXCHANGE_RATE_API_KEY')

# Load the API key from the environment
API_KEY = os.getenv('EXCHANGE_RATE_API_KEY')

# API endpoint and your API key (replace with your key)
API_URL = "https://v6.exchangerate-api.com/v6/YOUR_API_KEY/latest/USD"

if not API_KEY:
    raise ValueError("No API key found. Please set the EXCHANGE_RATE_API_KEY environment variable.")

# API endpoint and key
API_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"

def fetch_currency_data():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            rates = {
                'EUR': data['conversion_rates']['EUR'],
                'SEK': data['conversion_rates']['SEK']
            }
            return rates
        else:
            print(f"Error: API request failed with status code {response.status_code}")
            print(f"Response content: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def save_to_db(data):
    # Connect to SQLite database
    conn = sqlite3.connect('currency_data.db')
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS currency_rates (
            timestamp TEXT,
            EUR REAL,
            SEK REAL
        )
    ''')
    
    # Insert data into table
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO currency_rates (timestamp, EUR, SEK) VALUES (?, ?, ?)",
                   (timestamp, data['EUR'], data['SEK']))
    
    conn.commit()
    conn.close()

# Fetch and store the data every 5 minutes
if __name__ == "__main__":
    while True:
        currency_data = fetch_currency_data()
        if currency_data:
            save_to_db(currency_data)
        time.sleep(300)  # 5 minutes
