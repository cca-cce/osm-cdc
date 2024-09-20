# app.py

from flask import Flask, redirect, render_template
import random
import os

app = Flask(__name__)

# Set the path for the templates directory
app.template_folder = 'templates'

@app.route('/')
def index():
    # Randomly choose one of the two subpages
    page = random.choice(['page1', 'page2'])
    # Redirect to the selected subpage
    return redirect(f'/{page}')

@app.route('/page1')
def page1():
    return render_template('page1.html')

@app.route('/page2')
def page2():
    return render_template('page2.html')

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
