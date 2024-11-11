// Node.js Express application using JavaScript and SQLite

const fs = require('fs');
const express = require('express');
const session = require('express-session');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const uuid = require('uuid');
const bodyParser = require('body-parser');

const app = express();
const PORT = process.env.PORT || 5000;

// Set up SQLite Database
const db = new sqlite3.Database('ab_test_data.db', (err) => {
  if (err) {
    console.error('Error opening database:', err.message);
  } else {
    db.run(`CREATE TABLE IF NOT EXISTS ratings (
                session_id TEXT,
                ab_condition TEXT,
                image_set INTEGER,
                image_index INTEGER,
                image_name TEXT,
                rating INTEGER,
                timestamp INTEGER
            )`);
  }
});

// Middleware
app.use(express.static(path.join(__dirname, 'static')));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(
  session({
    secret: 'your_secret_key',
    resave: false,
    saveUninitialized: true,
  })
);

// Helper function to get or create a session ID
function getSessionId(req) {
  if (!req.session.session_id) {
    req.session.session_id = uuid.v4();
  }
  return req.session.session_id;
}

// Randomly assign A/B test condition and image set
function initializeUser(req) {
  req.session.ab_condition = req.session.ab_condition || (Math.random() < 0.5 ? 'A' : 'B');
  req.session.image_set = req.session.image_set || Math.floor(Math.random() * 20) + 1;
  req.session.current_image_index = req.session.current_image_index || 0;
  req.session.ab_test_completed = req.session.ab_test_completed || false;
  req.session.timestamp = req.session.timestamp || Date.now();
}

// Load images from the assigned image set
function loadImages(imageSet) {
  const folderPath = path.join(__dirname, 'static/images/set_' + imageSet);
  return fs.readdirSync(folderPath).filter((file) => file.match(/\.(png|jpg|jpeg)$/i)).map((file) => path.join('images/set_' + imageSet, file));
}

// Load A/B test images
function loadAbImages() {
  const folderPath = path.join(__dirname, 'static/condition');
  return fs.readdirSync(folderPath).filter((file) => file.match(/\.(png|jpg|jpeg)$/i)).map((file) => path.join('condition', file));
}

// Save rating to the database
function saveRating(sessionId, abCondition, imageSet, imageIndex, imageName, rating, timestamp) {
  db.run(
    `INSERT INTO ratings (session_id, ab_condition, image_set, image_index, image_name, rating, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)`,
    [sessionId, abCondition, imageSet, imageIndex, imageName, rating, timestamp],
    (err) => {
      if (err) {
        console.error('Error saving rating:', err.message);
      }
    }
  );
}

// Routes
app.get('/', (req, res) => {
  getSessionId(req);
  initializeUser(req);
  res.redirect('/ab_test');
});

app.get('/ab_test', (req, res) => {
  const abImages = loadAbImages();
  const abImagePath = req.session.ab_condition === 'A' ? abImages[0] : abImages[1];

  res.send(`
    <html>
      <head><title>A/B Test</title></head>
      <body>
        <h1>A/B Test</h1>
        <p>You are in condition: ${req.session.ab_condition}</p>
        <img src="/${abImagePath}" alt="A/B Test Image">
        <form method="post" action="/ab_test">
          <button type="submit">Proceed to Image Set</button>
        </form>
      </body>
    </html>
  `);
});

app.post('/ab_test', (req, res) => {
  req.session.ab_test_completed = true;
  res.redirect('/rate_image');
});

app.get('/rate_image', (req, res) => {
  const images = loadImages(req.session.image_set);
  const currentIndex = req.session.current_image_index;

  if (currentIndex >= images.length) {
    return res.send('<h1>Thank You!</h1><p>Thank you for participating in the survey!</p>');
  }

  const imagePath = images[currentIndex];
  const imageName = path.basename(imagePath);

  res.send(`
    <html>
      <head><title>Rate Image</title></head>
      <body>
        <h1>Rate Image ${currentIndex + 1}</h1>
        <img src="/${imagePath}" alt="Image to Rate">
        <form method="post" action="/rate_image">
          <label for="rating">Rate this image (1-7):</label>
          <select name="rating" id="rating" required>
            ${[1, 2, 3, 4, 5, 6, 7].map((i) => `<option value="${i}">${i}</option>`).join('')}
          </select>
          <button type="submit">Submit Rating</button>
        </form>
      </body>
    </html>
  `);
});

app.post('/rate_image', (req, res) => {
  const images = loadImages(req.session.image_set);
  const currentIndex = req.session.current_image_index;

  if (currentIndex >= images.length) {
    return res.redirect('/rate_image');
  }

  const imagePath = images[currentIndex];
  const imageName = path.basename(imagePath);
  const rating = parseInt(req.body.rating, 10);

  saveRating(req.session.session_id, req.session.ab_condition, req.session.image_set, currentIndex, imageName, rating, req.session.timestamp);
  req.session.current_image_index += 1;
  res.redirect('/rate_image');
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
