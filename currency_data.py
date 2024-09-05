import requests
import sqlite3
import time

# API endpoint and your API key (replace with your key)
API_URL = "https://v6.exchangerate-api.com/v6/YOUR_API_KEY/latest/USD"

def fetch_currency_data():
    response = requests.get(API_URL)
    data = response.json()
    if response.status_code == 200:
        # Extract EUR and SEK compared to USD
        rates = {
            'EUR': data['conversion_rates']['EUR'],
            'SEK': data['conversion_rates']['SEK']
        }
        return rates
    else:
        print("Error fetching data.")
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
