from flask import Flask, render_template, request, redirect, url_for, session
import random
import sqlite3
import uuid
import time
import os
from PIL import Image

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize SQLite Database
conn = sqlite3.connect('ab_test_data.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS ratings (
                session_id TEXT,
                ab_condition TEXT,
                image_set INTEGER,
                image_index INTEGER,
                image_name TEXT,
                rating INTEGER,
                timestamp INTEGER
            )''')
conn.commit()

# Helper function to get or create a session ID
def get_session_id():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']

# Randomly assign A/B test condition and image set
def initialize_user():
    if 'ab_condition' not in session:
        session['ab_condition'] = random.choice(['A', 'B'])
    if 'image_set' not in session:
        session['image_set'] = random.randint(1, 20)
    if 'current_image_index' not in session:
        session['current_image_index'] = 0
    if 'ab_test_completed' not in session:
        session['ab_test_completed'] = False
    if 'timestamp' not in session:
        session['timestamp'] = int(time.time() * 1000)

# Load images from the assigned image set
def load_images(image_set):
    folder_path = f'static/images/set_{image_set}'
    images = [os.path.join(folder_path, img) for img in os.listdir(folder_path) if img.endswith(('.png', '.jpg', '.jpeg'))]
    return images

# Load A/B test images
def load_ab_images():
    folder_path = 'static/condition'
    images = [os.path.join(folder_path, img) for img in os.listdir(folder_path) if img.endswith(('.png', '.jpg', '.jpeg'))]
    return images

# Save rating to the database
def save_rating(session_id, ab_condition, image_set, image_index, image_name, rating, timestamp):
    c.execute('INSERT INTO ratings (session_id, ab_condition, image_set, image_index, image_name, rating, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)',
              (session_id, ab_condition, image_set, image_index, image_name, rating, timestamp))
    conn.commit()

@app.route('/')
def index():
    # Initialize user session
    get_session_id()
    initialize_user()

    if not session['ab_test_completed']:
        return redirect(url_for('ab_test'))
    else:
        return redirect(url_for('rate_image'))

@app.route('/ab_test', methods=['GET', 'POST'])
def ab_test():
    ab_images = load_ab_images()
    if session['ab_condition'] == 'A':
        ab_image_path = ab_images[0]
    else:
        ab_image_path = ab_images[1]

    if request.method == 'POST':
        session['ab_test_completed'] = True
        return redirect(url_for('rate_image'))

    return render_template('ab_test.html', ab_image_path=ab_image_path, ab_condition=session['ab_condition'])

@app.route('/rate_image', methods=['GET', 'POST'])
def rate_image():
    images = load_images(session['image_set'])
    current_index = session['current_image_index']

    if current_index >= len(images):
        return render_template('thank_you.html')

    image_path = images[current_index]
    image_name = os.path.basename(image_path)

    if request.method == 'POST':
        rating = int(request.form['rating'])
        save_rating(session['session_id'], session['ab_condition'], session['image_set'], current_index, image_name, rating, session['timestamp'])
        session['current_image_index'] += 1
        return redirect(url_for('rate_image'))

    return render_template('rate_image.html', image_path=image_path, image_number=current_index + 1)

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)



