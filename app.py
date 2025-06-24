from flask import Flask, request, redirect, url_for, render_template
import os
import boto3
from dotenv import load_dotenv
from datetime import datetime
import sqlite3

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
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'm4a', 'flac'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize SQLite DB
DB_FILE = 'uploads.db'
with sqlite3.connect(DB_FILE) as conn:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            url TEXT NOT NULL,
            genre TEXT,
            structure TEXT,
            timestamp TEXT
        )
    ''')

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
            print(f"Genre: {selected_genre}, Structure: {selected_structure}")
            
            # 🗃 Save to SQLite DB
            with sqlite3.connect(DB_FILE) as conn:
                conn.execute('''
                    INSERT INTO uploads (filename, url, genre, structure, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                ''', (filename, url, selected_genre, selected_structure, datetime.now().isoformat()))
            
            return f'''
             File uploaded: {filename}<br>
             Genre: {selected_genre}<br>
             Structure: {selected_structure}<br>
             URL: <a href="{url}" target="_blank">{url}</a>
            '''
        else:
            return '🚫 File type not allowed'
    return render_template('upload.html')

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)