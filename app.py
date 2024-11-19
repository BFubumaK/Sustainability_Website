import os
import secrets

import psycopg2
from flask import Flask, render_template, request

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(16))

# List of buildings
buildings = [
    'MB1',
    'MB2',
    'MB3',
    'MB4',
    'MB5',
    'MA1',
    'MA2',
    'MA3',
    'MA4',
    'MA5',
    'LB1',
    'LB2',
    'LB3',
    'LB4',
    'LB5',
    'LA1',
    'LA2',
    'LA3',
    'LA4',
    'LA5'
]

# Define meter mappings by building
meters_by_building = {
    'MB1': ['lincoln_hall_main', 'hale_kuahine_main', 'korean_studies_main', 'hale_laulima_main', 'archtecture_main', 'hale_kahawai_main'],
    'MB2': ['gilmore_hall_main_a', 'gilmore_hall_main_b', 'gilmore_hall_mcc', 'ag_engineering_main', 'ag_engineering_mcc', 'webster_hall_main'],
    'MB3': ['hig_noaa', 'hig_panel_pb', 'hig_panel_pba', 'hig_substation_1_main', 'hig_substation_2_main', 'hig_substation_3_main', 'sakamaki_hall_ac_eqpt', 'sakamaki_hall_main'],
    'LB4': ['saunders_hall_main_a', 'saunders_hall_main_b', 'bus_ad_shidler_main', 'george_hall_main', 'crawford_hall_main', 'admin_serv_1', 'campus_ctr_main', 'hemenway_hall_kitchen', 'hemenway_hall_main']
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
