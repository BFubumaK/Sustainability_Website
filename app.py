import os
import secrets

import psycopg2
from flask import Flask, render_template, request

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(16))

# List of Buildings
buildings = [
    'ADMINISTRATIVE SERVICES BUILDING 1',
    'ADMINISTRATIVE SERVICES BUILDING 2',
    'AGRICULTURAL ENGINEERING INSTITUTE',
    'AGRICULTURAL SCIENCE BUILDING',
    'ANDREWS OUTDOOR THEATRE',
    'ARCHITECTURE BUILDING',
    'BACHMAN HALL',
    'BIOMEDICAL SCIENCES BUILDING',
    'BUILDING 37 - iLab',
    'VARSITY BUILDING',
    'JOHN A. BURNS HALL',
    'BUSINESS ADMINISTRATION BUILDING - SHIDLER',
    'CAMPUS CENTER',
    'UH CANCER CENTER FREEZER FACILITY',
    'CLARENCE TC CHING ATHLETICS COMPLEX',
    'Cloning Laboratory',
    'DANIEL K. INOUYE CENTER FOR MICROBIAL OCEANOGRAPHY: RESEARCH AND EDUCATION (C-MORE)',
    'CRAWFORD HALL',
    'DANCE BUILDING',
    'DEAN HALL',
    'DUKE KAHANAMOKU AQUATIC COMPLEX (DKAC)',
    'EDMONDSON HALL',
    'ENVIRONMENTAL PROTECTION FACILITY',
    'EVERLY HALL',
    'FREAR HALL',
    'GARTLEY HALL',
    'GATEWAY HOUSE',
    'GEORGE HALL',
    'GILMORE HALL',
    'HALE ALOHA - ILIMA TOWER',
    'HALE ALOHA - LEHUA TOWER',
    'HALE ALOHA - LOKELANI TOWER',
    'HALE ALOHA - MOKIHANA TOWER',
    'HALE HALAWAI',
    'HALE KAHAWAI',
    'HALE KUAHINE',
    'HALE LAULIMA',
    'HALE MANOA',
    'HALE NOELANI TOWER A',
    'HALE NOELANI TOWER B',
    'HALE NOELANI TOWER C',
    'HALE NOELANI TOWER D',
    'HALE NOELANI TOWER E',
    'HALE WAINANI F TOWER',
    'HALE WAINANI G TOWER',
    'HALE WAINANI H TOWER',
    'HALE WAINANI I TOWER',
    'HAMILTON LIBRARY',
    'HAWAII HALL',
    'HEMENWAY HALL',
    'HAWAII INSTITUTE OF GEOPHYSICS',
    'Health and Physical Education and Recreation Klum Gym',
    'Health and Physical Education and Recreation Main',
    'HOLMES HALL',
    'JEFFERSON HALL',
    'JOHNSON HALL A',
    'JOHNSON HALL B',
    'KELLER HALL',
    'KENNEDY THEATRE',
    'CENTER FOR KOREAN STUDIES',
    'KRAUSS HALL',
    'KUYKENDALL HALL',
    'LAW LIBRARY',
    'LAW SCHOOL',
    'LES MURAKAMI STADIUM',
    'LIFE SCIENCES BUILDING',
    'LINCOLN HALL',
    'MAINTENANCE SHOPS',
    'MALAMA 1-2 - ENVIRONMENTAL HEALTH AND SAFETY OFFICE',
    'MALAMA 3-4 - DIVE SAFETY',
    'MARINE SCIENCES BUILDING',
    'MILLER HALL',
    'MOORE HALL',
    'UNIVERSITY LAB SCHOOL - MULTIPURPOSE BUILDING',
    'Music Building Complex',
    'Pamoa Building',
    'PARADISE PALMS CAFE',
    'LOWER CAMPUS PARKING STRUCTURE - PHASE I',
    'LOWER CAMPUS PARKING STRUCTURE - PHASE II',
    'PACIFIC BIOSCIENCES RESEARCH CENTER (PBRC)',
    'PHYSICAL PLANT BUILDING',
    'PHYSICAL SCIENCE BUILDING',
    'POPE LABORATORY',
    'PACIFIC OCEAN SCIENCE AND TECHNOLOGY (POST)',
    'QUEEN LILIUOKALANI CENTER FOR STUDENT SERVICES',
    'Quad Chiller Plant',
    'SAKAMAKI HALL',
    'SAUNDERS HALL',
    'SHERMAN LABORATORY',
    'SINCLAIR LIBRARY',
    'Softball Tennis',
    'SPALDING HALL',
    'St. John Plant Science Lab',
    'STAN SHERIFF CENTER',
    'UNIVERSITY HEALTH SERVICES',
    'UNIVERSITY HIGH SCHOOL 3 - CLASSROOM BUILDING',
    'WARRIOR RECREATION CENTER',
    'WEBSTER HALL',
    'WIST HALL ANNEX 1',
    'WIST HALL'
]

# Define meter mappings by Building
meters_by_building = {
    'ADMINISTRATIVE SERVICES BUILDING 1': ['admin_serv_1'],
    'ADMINISTRATIVE SERVICES BUILDING 2': ['admin_serv_2'],
    'AGRICULTURAL ENGINEERING INSTITUTE': ['ag_engineering_main', 'ag_engineering_mcc'],
    'AGRICULTURAL SCIENCE BUILDING': ['ag_science_main_1', 'ag_science_main_2', 'ag_science_mcc'],
    'ANDREWS OUTDOOR THEATRE': ['andrews_amp_main'],
    'ARCHITECTURE BUILDING': ['archtecture_main'],
    'BACHMAN HALL': ['bachman_hall_main'],
    'BIOMEDICAL SCIENCES BUILDING': ['biomedical_science_ch_1', 'biomedical_science_ch_2', 'biomedical_science_main_a', 'biomedical_science_main_b', 'biomedical_science_mcc_a'],
    'BUILDING 37 - iLab': ['building_037_main'],
    'VARSITY BUILDING': ['building_1171a_to_f_main', 'building_1171f_cds']
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
    # Pass the list of Buildings to the template
    return render_template('visualization.html', Buildings=buildings)


# API to handle meter data based on selected Building
@app.route('/get_meters_for_building', methods=['POST'])
def get_meters_for_building():
    Building = request.form.get('Building_name')
    meters_for_Building = meters_by_building.get(Building, [])
    return {'meters': meters_for_Building}


if __name__ == '__main__':
    app.run(debug=True)
