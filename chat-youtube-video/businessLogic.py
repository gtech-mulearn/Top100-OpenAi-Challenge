import tempfile
from pprint import pprint

import whisper
from pytube import YouTube
from openai import OpenAI
import os


def transcribeVideoOrchestrator(youtube_url: str,  model_name: str):
    # audio = downloadYoutubeVideo(youtube_url)
    audio = downloadYoutubeAudio(youtube_url)
    # transcription = transcribe(audio, model_name)
    transcription = transcribeAPI(audio, model_name)
    return transcription


def transcribe(audio: dict, model_name="medium"):
    print("Transcribing...", audio['name'])
    print("Using model:", model_name)
    model = whisper.load_model(model_name)
    result = model.transcribe(audio['path'], )
    pprint(result)
    return result["text"]

def transcribeAPI(audio: dict, model_name="whisper-1"):
    print("Transcribing...", audio['name'])
    print("Using model:", model_name)
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    print(os.environ.get("OPENAI_API_KEY"))
    audio_file= open(audio['path'], "rb")
    result = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file,
    response_format="text"
    )
    pprint(result)
    return result["text"]

def downloadYoutubeVideo(youtube_url: str) -> dict:
    print("Processing : " + youtube_url)
    yt = YouTube(youtube_url)
    directory = tempfile.gettempdir()
    file_path = yt.streams.filter( progressive=True, file_extension='mp4').order_by(
        'resolution').desc().first().download(directory)
    print("VIDEO NAME " + yt._title)
    print("Download complete:" + file_path)
    return {"name": yt._title, "thumbnail": yt.thumbnail_url, "path": file_path}


def downloadYoutubeAudio(youtube_url: str) -> dict:
    print("Processing : " + youtube_url)
    yt = YouTube(youtube_url)
    directory = tempfile.gettempdir()
    
    # Choose the stream with the audio only (MP3 format)
    audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
    
    # Download the audio stream
    file_path = audio_stream.download(directory)
    
    print("AUDIO NAME: " + yt.title)
    print("Download complete:" + file_path)
    
    return {"name": yt.title, "thumbnail": yt.thumbnail_url, "path": file_path}


def on_progress(stream, chunk, bytes_remaining):
    """Callback function"""
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    pct_completed = bytes_downloaded / total_size * 100
    print(f"Status: {round(pct_completed, 2)} %")
