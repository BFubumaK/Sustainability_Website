import os
import secrets
import psycopg2
from flask import Flask, render_template, request

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(16))

# Sample list of buildings (manually defined in this case)
# Ideally, you would pull these from the database or an external source
buildings = [
    'admin_serv_1',
    'admin_serv_2_main',
    'ag_engineering_main',
    'ag_engineering_mcc',
    'ag_science_main_1',
    'ag_science_main_2',
    'andrews_amp_main',
    'architecture_main',
    'bachman_hall_main',
    'biomedical_science_ch_1',
    'biomedical_science_ch_2',
    # Add the rest of your buildings here...
]

# Define meter mappings by building
meters_by_building = {
    'admin_serv_1': ['admin_serv_1'],
    'admin_serv_2_main': ['admin_serv_2_main'],
    'ag_engineering_main': ['ag_engineering_main'],
    'ag_engineering_mcc': ['ag_engineering_mcc'],
    'ag_science_main_1': ['ag_science_main_1'],
    'ag_science_main_2': ['ag_science_main_2'],
    # Add the rest of your meter mappings here...
}

# Database connection setup
def get_db_connection():
    # Connect to the postgres database
    conn = psycopg2.connect(database="postgres", user="postgres", password="Uhosremote!", port="5433")
    return conn

# Render home page
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

# Render database page with most recent KWH data, sorted by meter name
@app.route('/show_entire_csv_data', methods=['GET'])
def show_recent_data():
    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch only the most recent data (e.g., last 156 records) from the postgres schema
    cur.execute('SELECT datetime, meter_reading, meter_name, stuck FROM kwh.kwh_last24hrs ORDER BY datetime DESC LIMIT 156;')
    kwh = cur.fetchall()

    cur.close()
    conn.close()

    # Sort data by the meter name (3rd column, index 2)
    kwh_sorted = sorted(kwh, key=lambda entry: entry[2].lower())  # sort alphabetically by meter_name

    # Render template with sorted KWH data
    return render_template('entire_csv_data.html', kwh=kwh_sorted)

# Render visualization page
@app.route('/visualization', methods=['GET', 'POST'])
def visualization():
    # Pass the list of buildings to the template
    return render_template('visualization.html', buildings=buildings)

# API to handle meter data based on selected building
@app.route('/get_meters_for_building', methods=['POST'])
def get_meters_for_building():
    building = request.form.get('building_name')
    meters_for_building = meters_by_building.get(building, [])
    return {'meters': meters_for_building}

if __name__ == '__main__':
    app.run(debug=True)
