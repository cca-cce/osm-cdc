# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS from flask_cors
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

# Database file path
DATABASE = 'tracking.db'

# Initialize the database
def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        # Create tables with user and timestamp fields
        c.execute('''
            CREATE TABLE mouse_positions (
                url TEXT,
                x INTEGER,
                y INTEGER,
                user TEXT,
                timestamp TEXT
            )
        ''')
        c.execute('''
            CREATE TABLE click_positions (
                url TEXT,
                x INTEGER,
                y INTEGER,
                user TEXT,
                timestamp TEXT
            )
        ''')
        c.execute('''
            CREATE TABLE scroll_positions (
                url TEXT,
                scroll_position INTEGER,
                user TEXT,
                timestamp TEXT
            )
        ''')
        conn.commit()
        conn.close()

init_db()

@app.route('/track', methods=['POST'])
def track():
    data = request.json
    print("Received data:", data)  # Debugging: Print the received data
    url = data.get('url')
    user = data.get('user')
    x = data.get('x')
    y = data.get('y')
    scroll = data.get('scroll')
    table = data.get('table')
    
    # Get current timestamp in ISO 8601 format with millisecond precision
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    try:
        if table == 'mouse_positions':
            c.execute('INSERT INTO mouse_positions (url, x, y, user, timestamp) VALUES (?, ?, ?, ?, ?)', (url, x, y, user, timestamp))
        elif table == 'click_positions':
            c.execute('INSERT INTO click_positions (url, x, y, user, timestamp) VALUES (?, ?, ?, ?, ?)', (url, x, y, user, timestamp))
        elif table == 'scroll_positions':
            c.execute('INSERT INTO scroll_positions (url, scroll_position, user, timestamp) VALUES (?, ?, ?, ?)', (url, scroll, user, timestamp))
        
        conn.commit()
        print(f"Inserted data into {table}: success")  # Debugging: Print success message
    except Exception as e:
        print(f"Error inserting data into {table}: {e}")  # Debugging: Print any errors
    finally:
        conn.close()

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)


