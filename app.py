import os
import secrets

import psycopg2
from flask import Flask, render_template, request

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(16))

# List of buildings
buildings = [
    'Administration Services Building 1',
    'Administration Services Building 2',
    'Agricultural Engineering Institute',
    'Agricultural Science',
    'Andrews Outdoor Theatre',
    'Architecture School',
    'Bachman Hall',
    'Biomedical Sciences',
    'Building 37',
    'Building 1171',
    'Burns Hall',
    'Shidler College of Business',
    'Campus Center',
    'Cancer Center',
    'Clarence T. C. Ching Athletics Complex',
    'Cloning Laboratory',
    'C-MORE Hale (Center for Microbial Oceanography: Research and Education)',
    'Crawford Hall',
    'Dance Building',
    'Dean Hall',
    'Kahanamoku Pool',
    'Edmondson Hall',
    'Environmental Protection Facility',
    'Everly Hall',
    'Frear Hall',
    'Gartley Hall',
    'Gateway House',
    'George Hall',
    'Gilmore Hall',
    'Hale Aloha ʻIlima',
    'Hale Aloha Lehua',
    'Hale Aloha Lokelani',
    'Hale Aloha Mokihana',
    'HALE HALAWAI',
    'HALE KAHAWAI',
    'HALE KUAHINE',
    'HALE LAULIMA',
    'HALE MANOA',
    'HALE NOELANI',
    'HALE WAINANI',
    'HAMILTON LIBRARY',
    'HAWAII HALL',
    'HEMENWAY HALL',
    'HIG',
    'HPER KLUM',
    'HPER MAIN',
    'HOLMES HALL',
    'JEFFERSON HALL',
    'JOHNSON HALL',
    'KELLER HALL',
    'KENNEDY THEATRE',
    'KOREAN STUDIES',
    'KRAUSS HALL',
    'KUYKENDALL HALL',
    'LAW LIBRARY',
    'LAW SCHOOL',
    'LES MURAKAMI STADIUM',
    'LIFE SCIENCES',
    'LINCOLN HALL',
    'MAINTENANCE SHOP',
    'MALAMA EHSO',
    'MALAMA DIVE SAFETY',
    'MARINE SCIENCE',
    'MILLER HALL',
    'MOORE HALL',
    'MULTIPURPOSE BUILDING',
    'MUSIC COMPLEX',
    'PAMOA BLDG',
    'PARADISE PALMS',
    'PARKING STRUCTURE PHASE 1',
    'PARKING STRUCTURE PHASE 2',
    'PBRC MAIN A',
    'PBRC MAIN B',
    'PHYSICAL PLANT BLDG',
    'PHYSICAL SCIENCE',
    'POPE LAB',
    'POST',
    'QLCSS',
    'QUAD CHILLER PLANT',
    'SAKAMAKI HALL',
    'SAUNDERS HALL',
    'SHERMAN',
    'SINCLAIR LIB',
    'SOFTBALL TENNIS',
    'SPALDING HALL',
    'ST JOHN PLAN SCIENCE',
    'STAN SHERIFF CTR',
    'STUDENT HEALTH',
    'TRANSPORTATION SERVICES',
    'UNIV HIGH SCHOOL',
    'WARRIOR REC CTR',
    'WEBSTER HALL',
    'WIST ANNEX',
    'WIST HALL'
]

# Define meter mappings by building
meters_by_building = {
    'ADMIN SERV 1': ['admin_serv_1'],
    'ADMIN SERV 2': ['admin_serv_2'],
    'AG ENGINEERING': ['ag_engineering_main', 'ag_engineering_mcc'],
    'AG SCIENCE': ['ag_science_main_1', 'ag_science_main_2', 'ag_science_mcc']
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
