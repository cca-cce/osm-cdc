import streamlit as st
import random
import sqlite3
import uuid
import time
from PIL import Image
import os

# Initialize SQLite Database
conn = sqlite3.connect('ab_test_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS ratings (
                session_id TEXT,
                ab_condition TEXT,
                image_set INTEGER,
                image_index INTEGER,
                rating INTEGER,
                timestamp INTEGER
            )''')
conn.commit()

# Helper function to get or create a session ID
def get_session_id():
    if 'session_id' not in st.session_state:
        st.session_state['session_id'] = str(uuid.uuid4())
    return st.session_state['session_id']

# Randomly assign A/B test condition and image set
def initialize_user():
    if 'ab_condition' not in st.session_state:
        st.session_state['ab_condition'] = random.choice(['A', 'B'])
    if 'image_set' not in st.session_state:
        st.session_state['image_set'] = random.randint(1, 20)
    if 'current_image_index' not in st.session_state:
        st.session_state['current_image_index'] = 0
    if 'ratings' not in st.session_state:
        st.session_state['ratings'] = []
    if 'ab_test_completed' not in st.session_state:
        st.session_state['ab_test_completed'] = False
    if 'timestamp' not in st.session_state:
        st.session_state['timestamp'] = int(time.time() * 1000)

# Load images from the assigned image set
def load_images(image_set):
    folder_path = f'images/set_{image_set}'
    images = [os.path.join(folder_path, img) for img in os.listdir(folder_path) if img.endswith(('.png', '.jpg', '.jpeg'))]
    return images

# Load A/B test images
def load_ab_images():
    folder_path = 'condition'
    images = [os.path.join(folder_path, img) for img in os.listdir(folder_path) if img.endswith(('.png', '.jpg', '.jpeg'))]
    return images

# Save rating to the database
def save_rating(session_id, ab_condition, image_set, image_index, rating, timestamp):
    c.execute('INSERT INTO ratings (session_id, ab_condition, image_set, image_index, rating, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (session_id, ab_condition, image_set, image_index, rating, timestamp))
    conn.commit()

# Main Streamlit App
st.title("A/B Test Image Rating App")

# Initialize user session
session_id = get_session_id()
initialize_user()

# A/B Test Phase
if not st.session_state['ab_test_completed']:
    ab_images = load_ab_images()
    if st.session_state['ab_condition'] == 'A':
        ab_image_path = ab_images[0]
    else:
        ab_image_path = ab_images[1]

    ab_image = Image.open(ab_image_path)
    st.image(ab_image, caption=f"Condition {st.session_state['ab_condition']} Image")

    if st.button("Proceed to Image Set"):
        st.session_state['ab_test_completed'] = True

# Load images for the user's assigned set
if st.session_state['ab_test_completed']:
    images = load_images(st.session_state['image_set'])

    # Display the current image and rating scale
    if st.session_state['current_image_index'] < len(images):
        image_path = images[st.session_state['current_image_index']]
        image = Image.open(image_path)
        st.image(image, caption=f"Image {st.session_state['current_image_index'] + 1}")

        rating = st.slider("Rate this image (1-7):", 1, 7, 4)

        if st.button("Submit Rating"):
            # Save the rating
            save_rating(session_id, st.session_state['ab_condition'], st.session_state['image_set'], st.session_state['current_image_index'], rating, st.session_state['timestamp'])
            
            # Move to the next image
            st.session_state['current_image_index'] += 1

    # If all images are rated, thank the user
    if st.session_state['current_image_index'] >= len(images):
        st.write("Thank you for participating in the survey!")



