# Import required modules
from flask import Flask, request, render_template
import psycopg2
import os
import secrets

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(16))

# Database connection setup
def get_db_connection():
    # Connect to the postgres database
    conn = psycopg2.connect(database="postgres", user="postgres", password="Uhosremote!", port="5433")
    return conn

# Render home page
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

# Render database page with most recent KWH data
@app.route('/show_entire_csv_data', methods=['GET'])
def show_recent_data():
    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch only the most recent data (e.g., last 10 records) from the postgres schema
    cur.execute('SELECT datetime, meter_reading, meter_name, stuck FROM kwh.kwh ORDER BY datetime DESC LIMIT 10;')
    kwh = cur.fetchall()

    cur.close()
    conn.close()

    # Render template with KWH data
    return render_template('entire_csv_data.html', kwh=kwh)

# Render visualization page
@app.route('/visualization', methods=['GET', 'POST'])
def visualization():
    return render_template('visualization.html')

if __name__ == '__main__':
    app.run(debug=True)
