import os
import secrets

import psycopg2
from flask import Flask, render_template, request

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(16))

# List of Buildings
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
    'Hale Halawai',
    'Hale Kahawai',
    'Hale Kuahine',
    'Hale Laulima',
    'Hale Manoa',
    'Hale Noelani',
    'Hale Wainani',
    'Hamilton Library',
    'Hawaii Hall',
    'Hemenway Hall',
    'Hawaii Institute of Geophysics',
    'Health and Physical Education and Recreation Klum Gym',
    'Health and Physical Education and Recreation Main',
    'Holmes Hall',
    'Jefferson Hall',
    'Johnson Hall',
    'Keller Hall',
    'Kennedy Theatre',
    'Center for Korean Studies',
    'Krauss Hall',
    'Kuykendall Hall',
    'Law Library',
    'Law School',
    'Les Murakami Stadium',
    'Life Sciences',
    'Lincoln Hall',
    'Maintenance Shop',
    'Malama Environmental Health & Safety',
    'Malama Dive Safety',
    'Marine Sciences Building',
    'Miller Hall',
    'Moore Hall',
    'Multipurpose Building',
    'Music Building Complex',
    'Pamoa Building',
    'Paradise Palms',
    'Parking Structure Phase 1',
    'Parking Structure Phase 2',
    'Pacific Biosciences Research Center Main A',
    'Pacific Biosciences Research Center Main B',
    'Physical Plant Building',
    'Physical Science Building',
    'Pope Laboratory',
    'Pacific Ocean Science and Technology',
    'Queen Liliʻuokalani Center for Student Services',
    'Quad Chiller Plant',
    'Sakamaki Hall',
    'Saunders Hall',
    'Sherman Laboratory',
    'Sinclair',
    'Softball Tennis',
    'Spalding Hall',
    'St. John Plant Science Lab',
    'Stan Sheriff Center',
    'Health Services',
    'Transportation Services',
    'University High School',
    'Warrior Recreation Center',
    'Webster Hall',
    'Wist Annex 1',
    'Wist Hall'
]

# Define meter mappings by Building
meters_by_building = {
    'Administration Services Building 1': ['admin_serv_1'],
    'Administration Services Building 2': ['admin_serv_2'],
    'Agricultural Engineering Institute': ['ag_engineering_main', 'ag_engineering_mcc'],
    'Agricultural Science': ['ag_science_main_1', 'ag_science_main_2', 'ag_science_mcc'],
    'Andrews Outdoor Theatre': ['andrews_amp_main'],
    'Architecture School': ['archtecture_main'],
    'Bachman Hall': ['bachman_hall_main']
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
    kwh = cur.fetchall()  # Correct method call

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
