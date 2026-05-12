# Quizly Backend

A Django REST API that generates quizzes from YouTube videos using AI.

## Tech Stack

- **Django** - Backend Framework
- **Django REST Framework** - REST API
- **SimpleJWT** - JWT Authentication
- **yt-dlp** - YouTube Audio Download
- **Whisper AI** - Audio Transcription
- **Groq (LLaMA 3.3)** - Quiz Generation
- **SQLite** - Database

## Requirements

- Python 3.10+
- **FFMPEG** (must be installed globally!)

### Install FFMPEG

**Linux (Ubuntu/Pop OS)**
```bash
sudo apt install ffmpeg
```

**macOS**
```bash
brew install ffmpeg
```

**Windows**

Download from https://ffmpeg.org/download.html and add to PATH.

## Installation

1. Clone the repository
```bash
git clone <repository-url>
cd backend
```

2. Create and activate a virtual environment

**Linux/macOS**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create a `.env` file based on `.env.example`

5. Run migrations
```bash
python manage.py migrate
```

6. Create a superuser (optional)
```bash
python manage.py createsuperuser
```

7. Start the server
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
| Method | URL | Description |
|---|---|---|
| POST | `/api/register/` | Register a new user |
| POST | `/api/login/` | Login and set JWT cookies |
| POST | `/api/logout/` | Logout and delete cookies |
| POST | `/api/token/refresh/` | Refresh access token |

### Quiz Management
| Method | URL | Description |
|---|---|---|
| POST | `/api/quizzes/` | Create a new quiz from YouTube URL |
| GET | `/api/quizzes/` | Get all quizzes of the user |
| GET | `/api/quizzes/{id}/` | Get a single quiz |
| PATCH | `/api/quizzes/{id}/` | Update title and description |
| DELETE | `/api/quizzes/{id}/` | Delete a quiz |

## How it works

1. User submits a YouTube URL
2. **yt-dlp** downloads the audio from the video
3. **Whisper AI** transcribes the audio locally
4. **Groq (LLaMA 3.3)** generates a quiz with 10 questions from the transcript
5. Quiz is saved to the database and returned to the user