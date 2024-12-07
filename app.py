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
    'TRANSPORTATION SERVICES',
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
    'VARSITY BUILDING': ['building_1171a_to_f_main', 'building_1171f_cds'],
    'JOHN A. BURNS HALL': ['burns_hall_main'],
    'BUSINESS ADMINISTRATION BUILDING - SHIDLER': ['bus_ad_shidler_main'],
    'CAMPUS CENTER': ['campus_ctr_main'],
    'UH CANCER CENTER FREEZER FACILITY': ['cancer_ctr_frzr_facil_main'],
    'CLARENCE TC CHING ATHLETICS COMPLEX': ['ching_complex_main'],
    'Cloning Laboratory': ['cloning_lan_dp_n'],
    'DANIEL K. INOUYE CENTER FOR MICROBIAL OCEANOGRAPHY: RESEARCH AND EDUCATION (C-MORE)': ['cmore_hale_main'],
    'CRAWFORD HALL': ['crawford_hall_main'],
    'DANCE BUILDING': ['dance_bldg_main'],
    'DEAN HALL': ['dean_hall_main'],
    'DUKE KAHANAMOKU AQUATIC COMPLEX (DKAC)': ['dkac_pool_main'],
    'EDMONDSON HALL': ['edmonson_hall_main'],
    'ENVIRONMENTAL PROTECTION FACILITY': ['env_protection_main'],
    'EVERLY HALL': ['everly_hall_main'],
    'FREAR HALL': ['frear_hall_main'],
    'GARTLEY HALL': ['gartley_hall_main'],
    'GATEWAY HOUSE': ['gateway_house_main_a', 'gateway_house_main_b'],
    'GEORGE HALL': ['george_hall_main'],
    'GILMORE HALL': ['gilmore_hall_main_a', 'gilmore_hall_main_b'],
    'HALE ALOHA - ILIMA TOWER': ['hale_aloha_ilima_tower_cafe', 'hale_aloha_ilima_tower_main'],
    'HALE ALOHA - LEHUA TOWER': ['hale_aloha_lehua_tower_main'],
    'HALE ALOHA - LOKELANI TOWER': ['hale_aloha_lokelani_tower_main'],
    'HALE ALOHA - MOKIHANA TOWER': ['hale_aloha_mokihana_tower_main'],
    'HALE HALAWAI': ['hale_halawai_main'],
    'HALE KAHAWAI': ['hale_kahawai_main'],
    'HALE KUAHINE': ['hale_kuahine_main'],
    'HALE LAULIMA': ['hale_laulima_main'],
    'HALE MANOA': ['hale_manoa_main'],
    'HALE NOELANI TOWER A': ['hale_noelani_all_towers_main', 'hale_noelani_tower_a_b'],
    'HALE NOELANI TOWER B': ['hale_noelani_all_towers_main', 'hale_noelani_tower_a_b', 'hale_noelani_tower_b'],
    'HALE NOELANI TOWER C': ['hale_noelani_all_towers_main', 'hale_noelani_tower_c', 'hale_noelani_tower_c_d'],
    'HALE NOELANI TOWER D': ['hale_noelani_all_towers_main', 'hale_noelani_tower_c_d'],
    'HALE NOELANI TOWER E': ['hale_noelani_all_towers_main', 'hale_noelani_tower_e'],
    'HALE WAINANI F TOWER': ['hale_wainani_f_tower_main'],
    'HALE WAINANI G TOWER': ['hale_wainani_g_tower_main'],
    'HALE WAINANI H TOWER': ['hale_wainani_h_tower_main'],
    'HALE WAINANI I TOWER': ['hale_wainani_i_tower_main'],
    'HAMILTON LIBRARY': ['hamilton_lib_1_2_main_1', 'hamilton_lib_1_2_main_2', 'hamilton_lib_ph_iii_ch_1', 'hamilton_lib_ph_iii_ch_2', 'hamilton_lib_ph_iii_ch_3', 'hamilton_lib_ph_iii_main_1', 'hamilton_lib_ph_iii_main_2',
                         'hamilton_lib_ph_iii_main_3',
                         ],
    'HAWAII HALL': ['hawaii_hall_main'],
    'HEMENWAY HALL': ['hemenway_hall_kitchen', 'hemenway_hall_main'],
    'HAWAII INSTITUTE OF GEOPHYSICS': ['hig_noaa', 'hig_panel_pb', 'hig_panel_pba', 'hig_substation_1_main', 'hig_substation_2_main', 'hig_substation_3_main',
                                       ],
    'Health and Physical Education and Recreation Klum Gym': ['hper_klum_gym'],
    'Health and Physical Education and Recreation Main': ['hper_main'],
    'HOLMES HALL': [],
    'JEFFERSON HALL': ['jefferson_hall_main'],
    'JOHNSON HALL A': ['johnson_hall_a_main'],
    'JOHNSON HALL B': ['johnson_hall_b_main'],
    'KELLER HALL': ['keller_hall_main'],
    'KENNEDY THEATRE': ['kennedy_theatre_main'],
    'CENTER FOR KOREAN STUDIES': ['korean_studies_main'],
    'KRAUSS HALL': ['krauss_hall_main'],
    'KUYKENDALL HALL': ['kuykendall_hall_main'],
    'LAW LIBRARY': ['law_lib_main'],
    'LAW SCHOOL': ['law_school_main'],
    'LES MURAKAMI STADIUM': ['les_murakami_stadium_consess', 'les_murakami_stadium_main'],
    'LIFE SCIENCES BUILDING': ['life_sciences_dp2aec_2aec1', 'life_sciences_dp2aec_2bec1', 'life_sciences_dp2am_2am1', 'life_sciences_dp2am_2bm1', 'life_sciences_dp2am_2cm1', 'life_sciences_dp2am_2dm1', 'life_sciences_msb1_4a1',
                               'life_sciences_msb1_4b1', 'life_sciences_msb1_4c1', 'life_sciences_msb1_main', 'life_sciences_msb1_xmr2a', 'life_sciences_msb1_xmr2b', 'life_sciences_msb1_xmr2c', 'life_sciences_msb2_4dm', 'life_sciences_msb3_4des1',
                               'life_sciences_msb3_elev1', 'life_sciences_msb3_elev2', 'life_sciences_msb3_xmr2aes', 'life_sciences_msb3_xmr2bes', 'life_sciences_msb3_xmr2ces', 'life_sciences_msb4_4aec1', 'life_sciences_msb4_4bec1',
                               'life_sciences_msb4_4cec1',
                               ],
    'LINCOLN HALL': ['lincoln_hall_main'],
    'MAINTENANCE SHOPS': ['maintenance_shop_main'],
    'MALAMA 1-2 - ENVIRONMENTAL HEALTH AND SAFETY OFFICE': ['malama_1_2_ehso_main'],
    'MALAMA 3-4 - DIVE SAFETY': ['malama_3_4_dive_safety_main'],
    'MARINE SCIENCES BUILDING': ['marine_science_main_a', 'marine_science_main_b', 'marine_science_mcc'],
    'MILLER HALL': ['miller_hall_main'],
    'MOORE HALL': ['moore_hall_main'],
    'UNIVERSITY LAB SCHOOL - MULTIPURPOSE BUILDING': ['multipurpose_bldg_main'],
    'Music Building Complex': ['music_complex_main'],
    'Pamoa Building': ['pamoa_buildings_main'],
    'PARADISE PALMS CAFE': ['paradise_palms_main'],
    'LOWER CAMPUS PARKING STRUCTURE - PHASE I': ['parking_struct_ph_i_main'],
    'LOWER CAMPUS PARKING STRUCTURE - PHASE II': [],
    'PACIFIC BIOSCIENCES RESEARCH CENTER (PBRC)': ['pbrc_main_b'],
    'PHYSICAL PLANT BUILDING': ['physical_plant_bldg_main'],
    'PHYSICAL SCIENCE BUILDING': ['physical_science_keller_comp', 'physical_science_main'],
    'POPE LABORATORY': ['pope_lab_main'],
    'PACIFIC OCEAN SCIENCE AND TECHNOLOGY (POST)': ['post_chiller_plant_main', 'post_main_1', 'post_main_2'],
    'QUEEN LILIUOKALANI CENTER FOR STUDENT SERVICES': ['qlcss_main'],
    'Quad Chiller Plant': ['quad_chiller_plant_main'],
    'SAKAMAKI HALL': ['sakamaki_hall_ac_eqpt', 'sakamaki_hall_main'],
    'SAUNDERS HALL': ['saunders_hall_main_a', 'saunders_hall_main_b'],
    'SHERMAN LABORATORY': ['sherman_main_1', 'sherman_main_2'],
    'SINCLAIR LIBRARY': ['sinclair_lib_main'],
    'Softball Tennis': ['softball_tennis_main'],
    'SPALDING HALL': ['spalding_hall_main'],
    'St. John Plant Science Lab': ['st_john_plant_science_main'],
    'STAN SHERIFF CENTER': ['stan_sheriff_ctr_main_1', 'stan_sheriff_ctr_main_2'],
    'UNIVERSITY HEALTH SERVICES': ['student_health_main'],
    'TRANSPORTATION SERVICES': ['transportation_srvc_main'],
    'UNIVERSITY HIGH SCHOOL 3 - CLASSROOM BUILDING': ['univ_high_school_3_main'],
    'WARRIOR RECREATION CENTER': ['warrior_rec_ctr_main'],
    'WEBSTER HALL': ['webster_hall_main'],
    'WIST HALL ANNEX 1': ['wist_annex_1_main'],
    'WIST HALL': ['wist_hall_main']
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
