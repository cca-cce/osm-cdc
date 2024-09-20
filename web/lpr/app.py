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
    return """<h1>This is Page 1</h1>
<!-- Start Landing Page -->
      <div class="landing-page">
        <header>
          <div class="container">
            <a href="#" class="logo">Your <b>Website</b></a>
            <ul class="links">
              <li>Home</li>
              <li>About Us</li>
              <li>Work</li>
              <li>Info</li>
              <li>Get Started</li>
            </ul>
          </div>
        </header>
        <div class="content">
          <div class="container">
            <div class="info">
              <h1>Looking For Inspiration</h1>
              <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Repellendus odit nihil ullam nesciunt quidem iste, Repellendus odit nihil</p>
              <button>Call to action</button>
            </div>
            <div class="image">
              <img src="./001234.png">
            </div>
          </div>
        </div>
      </div>
      <!-- End Landing Page -->
"""

@app.route('/page2')
def page2():
    return '<h1>This is Page 2</h1>'

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)




