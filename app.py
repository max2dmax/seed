from flask import Flask, request, redirect, url_for, render_template
import os
import boto3
from dotenv import load_dotenv
from datetime import datetime
import sqlite3
import logging
import psycopg2
from urllib.parse import urlparse
logging.basicConfig(level=logging.DEBUG)

load_dotenv()

s3 = boto3.client('s3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

def upload_to_s3(file, filename):
    s3.upload_fileobj(
        file,
        os.getenv("S3_BUCKET_NAME"),
        filename,
        ExtraArgs={
            'ContentType': file.content_type
        }
    )
    url = f"https://{os.getenv('S3_BUCKET_NAME')}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{filename}"
    return url

# Create Flask app
app = Flask(__name__)

# Setup upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'm4a', 'flac', 'aiff'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DATABASE_URL = os.getenv('DATABASE_URL')  # Add this to your Render env variables

def init_db():
    result = urlparse(DATABASE_URL)
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port

    conn = psycopg2.connect(
        database=database,
        user=username,
        password=password,
        host=hostname,
        port=port
    )
    with conn:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS uploads (
                    id SERIAL PRIMARY KEY,
                    filename TEXT NOT NULL,
                    url TEXT NOT NULL,
                    genre TEXT,
                    structure TEXT,
                    timestamp TEXT
                )
            ''')
    conn.close()

init_db()

# Helper function
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Upload route
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    app.logger.debug("📥 /upload route triggered")
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part 🫠'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file 🫥'
        if file and allowed_file(file.filename):
            # Save file to S3
            filename = file.filename
            url = upload_to_s3(file, filename)

            # 👇 Grab dropdown values
            selected_genre = request.form.get('genre')
            selected_structure = request.form.get('structure')

            # 🎶 Log or use this data however you like
            app.logger.debug(f"Genre: {selected_genre}, Structure: {selected_structure}")
            
            # 🗃 Save to PostgreSQL DB
            try:
                app.logger.debug("🔥 Attempting to insert into DB!")
                app.logger.debug(f"➡️ filename: {filename}")
                app.logger.debug(f"➡️ url: {url}")
                app.logger.debug(f"➡️ genre: {selected_genre}")
                app.logger.debug(f"➡️ structure: {selected_structure}")
                app.logger.debug(f"➡️ timestamp: {datetime.now().isoformat()}")

                result = urlparse(DATABASE_URL)
                conn = psycopg2.connect(
                    dbname=result.path[1:],
                    user=result.username,
                    password=result.password,
                    host=result.hostname,
                    port=result.port
                )
                with conn:
                    with conn.cursor() as cur:
                        cur.execute('''
                            INSERT INTO uploads (filename, url, genre, structure, timestamp)
                            VALUES (%s, %s, %s, %s, %s)
                        ''', (filename, url, selected_genre, selected_structure, datetime.now().isoformat()))
                conn.close()

                app.logger.debug("✅ Upload record successfully inserted into database!")
                app.logger.debug(f"📍 DB URL: {DATABASE_URL}")
            except Exception as e:
                app.logger.error(f"🧨 DB Error: {e}")
            
            return f'''
             File uploaded: {filename}<br>
             Genre: {selected_genre}<br>
             Structure: {selected_structure}<br>
             URL: <a href="{url}" target="_blank">{url}</a>
            '''
        else:
            return '🚫 File type not allowed'
    return render_template('upload.html')

# History route
@app.route('/history')
def upload_history():
    app.logger.debug(f"🧠 Using DB URL: {DATABASE_URL}")
    result = urlparse(DATABASE_URL)
    conn = psycopg2.connect(
        dbname=result.path[1:],
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port
    )
    with conn:
        with conn.cursor() as cur:
            cur.execute('SELECT filename, url, genre, structure, timestamp FROM uploads ORDER BY timestamp DESC')
            uploads = cur.fetchall()
    conn.close()
    return render_template('history.html', uploads=uploads)

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
