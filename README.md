# Risk Analysis from Call Recordings

A Django web app that analyzes call recordings for emotional content and urgency, assigning risk priority ratings.

## Overview

Upload audio files → Transcribe with Whisper → Analyze sentiment → Classify via keywords → Assign priority → View results on dashboard.

### Key Features
- Audio upload and transcription
- Sentiment analysis
- Keyword-based categorization (emergency, crime, complaint, spam)
- Priority scoring (0-5)
- Dashboard with stats and recent calls

## System Workflow

```
User opens web application
           |
           v
User uploads audio OR records audio
           |
           v
User clicks "Analyze Call"
           |
           v
System shows loading screen
           |
           v
Audio is converted to text using Whisper
           |
           v
Transcript is cleaned and tokenized
           |
           v
Keywords are matched against predefined categories
           |
           v
Call intent is predicted
(Spam / Complaint / Crime / Emergency)
           |
           v
Emotion is inferred from predicted intent
           |
           v
Risk priority (0–5) is assigned
           |
           v
Explanation is generated using matched keywords
           |
           v
Analysis result is stored in database
           |
           v
Previous records and statistics are fetched
           |
           v
Result and dashboard are displayed to user
```

## Installation

### Prerequisites
- Python 3.8+
- pip
- FFmpeg

### Steps
1. Clone repo
2. Create venv: `python -m venv venv`
3. Activate: `venv\Scripts\activate`
4. Install deps: `pip install django openai-whisper textblob`
5. Migrate: `python manage.py migrate`
6. Run: `python manage.py runserver`
7. Open `http://127.0.0.1:8000/`

## Accessing the Database

To view and manage data via Django admin:

1. Create superuser: `python manage.py createsuperuser`
2. Run server: `python manage.py runserver`
3. Go to `http://127.0.0.1:8000/admin/` and log in

## Usage

- Upload audio file on home page
- Click "Analyze Call"
- View results: emotion, category, priority, explanation
- Dashboard shows stats and recent calls with audio playback

## API Endpoints

- `GET /` - Upload page
- `POST /analyze/` - Analyze audio
- `GET /admin/` - Django admin

## Technologies

- Django
- Whisper (STT)
- TextBlob (sentiment)
- SQLite

## Project Structure

```
risk-analysis-from-call-recordings/
├── backend/          # Django settings
├── calls/            # App with models, views, templates
├── media/            # Uploaded files
├── db.sqlite3        # Database
└── manage.py
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- FFmpeg (required for Whisper audio processing)

### Steps
1. **Clone the Repository**
   ```bash
   git clone https://github.com/DevanshRajani25/risk-analysis-from-call-recordings.git
   cd risk-analysis-from-call-recordings
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install django openai-whisper textblob
   ```

   Note: FFmpeg must be installed separately. Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

4. **Apply Migrations**
   ```bash
   python manage.py migrate
   ```

5. **Run the Server**
   ```bash
   python manage.py runserver
   ```

6. **Access the Application**
   Open your browser and go to `http://127.0.0.1:8000/`

## Usage

### Uploading and Analyzing Calls
1. Navigate to the home page.
2. Click "Choose File" to select an audio file (WAV/MP3).
3. Click "Analyze Call" to process the recording.
4. View the analysis results including emotion, category, priority, and explanation.
5. Listen to the audio playback directly on the dashboard.

### Dashboard Features
- **Current Call Result**: Detailed analysis of the latest uploaded call.
- **Statistics**: Overview of total calls and breakdown by category.
- **Recent Calls**: Table of the last 5 analyzed calls with audio controls.

## API Endpoints

- `GET /` - Upload page
- `POST /analyze/` - Analyze uploaded audio file
- `GET /admin/` - Django admin interface (requires superuser)

## Technologies Used

- **Backend**: Django 6.0
- **Database**: SQLite
- **AI/ML**:
  - Whisper (OpenAI) for speech-to-text
  - TextBlob for sentiment analysis
- **Frontend**: HTML, CSS (inline styling)
- **File Handling**: Django's FileField for uploads

## Project Structure

```
risk-analysis-from-call-recordings/
├── backend/                 # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── calls/                   # Main Django app
│   ├── models.py            # CallAnalysis model
│   ├── views.py             # Analysis logic
│   ├── urls.py              # App URLs
│   ├── templates/           # HTML templates
│   │   ├── upload.html
│   │   ├── dashboard.html
│   │   └── processing.html
│   └── migrations/          # Database migrations
├── media/                   # Uploaded files
├── db.sqlite3               # SQLite database
├── manage.py                # Django management script
└── README.md
```

