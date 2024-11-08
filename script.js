// Import required modules
const express = require('express');
const { Pool } = require('pg');
const path = require('path');
const bodyParser = require('body-parser');

// Create an Express application
const app = express();
const port = 3000; // default port

// Create a Postgres connection with schema 'kwh' and table 'kwh'
const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'postgres',
  password: 'Uhosremote!',
  port: 5433, // default port
});

// Middleware to serve static files
app.use(express.static(path.join(__dirname, '')));

// Middleware to parse URL-encoded bodies
app.use(bodyParser.urlencoded({ extended: false }));

// Set up route handler for home page
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// Route handler for GET KWH data (fetch only the 156 most recent records)
app.get('/kwh', (req, res) => {
  // SQL query to fetch data from schema 'kwh' and table 'kwh'
  const query = 'SELECT datetime, meter_reading, meter_name, stuck FROM kwh.kwh_last24hrs ORDER BY datetime DESC LIMIT 156;';

  pool.query(query, (error, result) => {
    if (error) {
      console.error('Error occurred:', error);
      res.status(500).send('An error occurred while retrieving data from the database.');
    } else {
      // Return the most recent KWH data as JSON
      const kwhData = result.rows;
      res.json(kwhData);
    }
  });
});

// Listen to requests
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
