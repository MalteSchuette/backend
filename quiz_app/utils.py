import yt_dlp
import os
import whisper
from groq import Groq
from django.conf import settings
import json


def download_audio(url, output_path='audio'):
    """Downloads audio from a YouTube URL and returns the local file path."""
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
    """Transcribes an audio file using Whisper AI and returns the transcript."""
    model = whisper.load_model('base')
    result = model.transcribe(file_path)
    return result['text']


def generate_quiz(transcript):
    """Generates a quiz with 10 questions and 4 options using Groq AI."""
    client = Groq(api_key=settings.GROQ_API_KEY)
    prompt = f"""Based on the following transcript, generate a quiz in valid JSON format.
The quiz must follow this exact structure:
{{
  "title": "Create a concise quiz title based on the topic of the transcript.",
  "description": "Summarize the transcript in no more than 150 characters. Do not include any quiz questions or answers.",
  "questions": [
    {{
      "question_title": "The question goes here.",
      "question_options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "The correct answer from the above options"
    }}
  ]
}}
Requirements:
- Each question must have exactly 4 distinct answer options.
- Only one correct answer is allowed per question, and it must be present in 'question_options'.
- The output must be valid JSON and parsable as-is (e.g., using Python's json.loads).
- Do not include explanations, comments, or any text outside the JSON.
- Generate all text (title, description, questions and answers) in the same language as the transcript.

Transcript:
{transcript}"""
    response = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[{'role': 'user', 'content': prompt}],
        response_format={'type': 'json_object'},
    )
    return json.loads(response.choices[0].message.content)

def process_youtube_url(url):
    """Full pipeline: downloads audio, transcribes it and generates a quiz."""
    audio_file = download_audio(url)
    transcript = transcribe_audio(audio_file)
    quiz_data = generate_quiz(transcript)
    os.remove(audio_file)
    return quiz_data