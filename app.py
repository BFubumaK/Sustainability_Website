from flask import Flask, request, render_template
import pandas as pd
import os
import secrets

# Setup for file upload
UPLOAD_FOLDER = os.path.join('staticFiles', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1000 * 1024 * 1024  # 1000 MB limit
app.secret_key = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(16))  # key


# Render home page
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


# Render database page with CSV data
@app.route('/show_entire_csv_data', methods=['GET'])
def show_entire_csv_data():
    permanent_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'kwh.csv')

    try:
        uploaded_df = pd.read_csv(permanent_file_path, encoding='unicode_escape')
        uploaded_df['datetime'] = pd.to_datetime(uploaded_df['datetime'], format='%m/%d/%Y %H:%M')
        for col in uploaded_df.select_dtypes(include='number').columns:
            if uploaded_df[col].dtype == 'float64':
                uploaded_df[col] = uploaded_df[col].apply(
                    lambda x: str(x).rstrip('0').rstrip('.') if pd.notnull(x) else '')

        # Get the date filter from the request
        filter_date = request.args.get('date')
        if filter_date:
            uploaded_df = uploaded_df[uploaded_df['datetime'].dt.date == pd.to_datetime(filter_date).date()]

        # Pagination logic
        page = request.args.get('page', 1, type=int)
        per_page = 50
        start = (page - 1) * per_page
        end = start + per_page
        paginated_df = uploaded_df.iloc[start:end]

        # Group data by meter name and prepare HTML tables
        meter_groups = paginated_df.groupby('meter_name')
        tables_html = {
            meter_name: group.to_html(index=False, classes='table table-striped table-bordered', escape=False)
            for meter_name, group in meter_groups
        }

        # Calculate total pages for pagination
        total_pages = (len(uploaded_df) + per_page - 1) // per_page

    except Exception as e:
        return f"Error reading CSV: {e}", 500

    # Render entire_csv_data.html
    return render_template('entire_csv_data.html', tables=tables_html, page=page, total_pages=total_pages)


# Render visualization page
@app.route('/visualization', methods=['GET', 'POST'])
def visualization():
    return render_template('visualization.html')


if __name__ == '__main__':
    app.run(debug=True)
