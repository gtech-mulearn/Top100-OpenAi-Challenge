import tempfile
from pprint import pprint
from pydub import AudioSegment
import whisper
from pytube import YouTube
from openai import OpenAI
import io
import os
from typing import Union
import streamlit as st

client = OpenAI()

def transcribeVideoOrchestrator(youtube_url: str,  model_name: str):
    # audio = downloadYoutubeVideo(youtube_url)
    audio = downloadYoutubeAudio(youtube_url)
    # transcription = transcribe(audio, model_name)
    transcription = transcribeAPI(audio, model_name)
    topics = discoverTopics(transcription)
    analysis = analyseTopics(topics)
    result = {
        "transcription": transcription,
        "topics": topics,
        "analysis": analysis
    }
    return result


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
    print(client.api_key)
    audio_file= open(audio['path'], "rb")
    result = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file,
    response_format="text"
    )
    pprint(result)
    return result

    # print("Transcribing...", audio_path)
    print("Using model:", model_name)
    
    try:
        if isinstance(audio, st.uploaded_file_manager.UploadedFile):
            # If audio is an UploadedFile object from Streamlit
            audio_path = save_uploaded_file(audio)
        elif isinstance(audio, str):
            # If audio is already a file path
            audio_path = audio
        else:
            raise ValueError("Invalid audio input")

        print("Transcribing...", audio_path)
        print("Using model:", model_name)

        with open(audio_path, "rb") as audio_file:
            result = client.audio.transcriptions.create(
                model=model_name,
                file=audio_file,
                response_format="text"
            )
            pprint(result)
            return result


    except Exception as e:
        print(f"Error occurred during transcription: {str(e)}")
        return None
    


def discoverTopics(text: str, model_name = "gpt-3.5-turbo"):
    print("Points Summarizing...")
    print("Using model:", model_name)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to summarize text using bullet points and appropriate topics."},
            {"role": "user", "content": text}
            ],
        temperature=0,
        max_tokens=1024
    )
    pprint(response.choices[0].message.content)
    return response.choices[0].message.content

def analyseTopics(text: str, model_name = "gpt-3.5-turbo"):
    print("Content Analysing...")
    print("Using model:", model_name)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Analyse content for: Spam, deceptive practices and scams, Sensitive content, Child safety , Nudity and sexual content, Suicide and self-harm , Vulgar language, etc. If yes, give reason. If no, say what type of content the text has."},
            {"role": "user", "content": text}
            ],
        temperature=0,
        max_tokens=1024
    )
    pprint(response.choices[0].message.content)
    return response.choices[0].message.content

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
