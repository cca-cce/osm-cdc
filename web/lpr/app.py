# app.py

from flask import Flask, redirect
import random

app = Flask(__name__)

@app.route('/')
def index():
    # Randomly choose one of the two subpages
    page = random.choice(['page1', 'page2'])
    # Redirect to the selected subpage
    return redirect(f'/{page}')

@app.route('/page1')
def page1():
    return '<h1>This is Page 1</h1>'

@app.route('/page2')
def page2():
    return '<h1>This is Page 2</h1>'

if __name__ == '__main__':
    app.run(debug=True)




