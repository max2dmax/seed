# SEED — AI Song Framework Generator

Welcome to SEED, a web app that helps you grow full-length instrumentals from a single spark — like a musical seed.  
Upload your idea, choose your vibe, and SEED handles the rest.

## What It Does

SEED is a Flask-powered app that:
- Accepts audio uploads (like .mp3, .wav, .m4a)
- Uploads files to AWS S3 for storage
- Collects genre and song structure selections from the user
- Saves all relevant metadata to a PostgreSQL database
- (Coming soon) Uses AI to generate full instrumentals from the uploaded idea

## Tech Stack

| Component      | Tech Used           |
|----------------|---------------------|
| Frontend       | HTML + CSS (styled like a guitar pedal) |
| Backend        | Flask (Python)      |
| File Storage   | AWS S3              |
| Database       | PostgreSQL (via Render) |
| Hosting        | Render.com          |
| Logging        | Python logging      |

## Project Structure

```
seed/
├── static/                  # Optional CSS, JS, etc.
├── templates/               # HTML templates (Jinja2)
│   └── upload.html          # Main upload UI
├── app.py                   # The Flask app
├── requirements.txt         # Python dependencies
├── .gitignore               # Ignores secrets and system files
├── .env                     # Environment secrets (never committed)
└── README.md                # This file
```

## Environment Variables

Set the following in Render’s Environment tab:

```
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
S3_BUCKET_NAME=your-bucket-name
S3_REGION=us-east-1
DATABASE_URL=your-postgres-url
```

## Setup Instructions

1. Clone the repo
2. Set your environment variables in `.env`
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the app locally:
   ```
   flask run
   ```

## Features

- Upload files and metadata
- Store them in AWS S3
- Save structured info to a live database
- View real-time logs and debug info in terminal

## Coming Soon

- AI-generated full instrumentals
- User accounts and history
- Preview before upload
- Download completed tracks

## Made with care

Built by Max for musicians who want to turn sparks into songs.