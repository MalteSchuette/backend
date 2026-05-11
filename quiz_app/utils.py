import yt_dlp
import os
import whisper
from google import genai
from django.conf import settings
import json


def download_audio(url, output_path='audio'):
    os.makedirs(output_path, exist_ok=True)
    tmp_filename = f'{output_path}/%(id)s.%(ext)s'
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': tmp_filename,
        'quiet': True,
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = f"{output_path}/{info['id']}.{info['ext']}"
        return filename
    

def transcribe_audio(file_path):
    model = whisper.load_model('base')
    result = model.transcribe(file_path)
    return result['text']


def generate_quiz(transcript):
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    prompt = f"""
    Based on the following transcript, generate a quiz with exactly 10 questions.
    Each question must have exactly 4 answer options and one correct answer.
    
    Return ONLY a JSON array in this exact format, nothing else:
    [
        {{
            "question_title": "Question text here",
            "question_options": ["Option A", "Option B", "Option C", "Option D"],
            "answer": "Option A"
        }}
    ]
    
    Transcript:
    {transcript}
    """
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt
    )
    print("Raw response from Gemini API:", response.text)  # Debugging line
    cleaned = response.text.strip().removeprefix('```json').removesuffix('```').strip()
    print("Cleaned response:", cleaned)  # Debugging line
    return json.loads(cleaned)