import tempfile
from pprint import pprint
import whisper
from pytube import YouTube
from openai import OpenAI
from urllib.parse import urlparse, parse_qs

# client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
client = OpenAI()


def get_video_id(youtube_url):
    # Parse the URL to get the query parameters
    parsed_url = urlparse(youtube_url)
    query_params = parse_qs(parsed_url.query)

    # Extract the video ID from the 'v' parameter
    video_id = query_params.get('v', [''])[0]

    return video_id

def transcribeVideoOrchestrator(youtube_url: str,  model_name = "tiny"):
    # audio = downloadYoutubeVideo(youtube_url)
    audio = downloadYoutubeAudio(youtube_url)
    # transcription = getTranscriptionsFromModel(audio, model_name)
    transcription = getTranscriptionsFromAPI(audio, model_name)
    topics = discoverTopics(transcription)
    analysis = analyseTopics(topics)
    result = {
        "transcription": transcription,
        "topics": topics,
        "analysis": analysis
    }
    return result

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


def getTranscriptionsFromAPI(audio: dict, model_name="whisper-1"):
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


# def downloadYoutubeVideo(youtube_url: str) -> dict:
#     print("Processing : " + youtube_url)
#     yt = YouTube(youtube_url)
#     directory = tempfile.gettempdir()
#     file_path = yt.streams.filter( progressive=True, file_extension='mp4').order_by(
#         'resolution').desc().first().download(directory)
#     print("VIDEO NAME " + yt._title)
#     print("Download complete:" + file_path)
#     return {"name": yt._title, "thumbnail": yt.thumbnail_url, "path": file_path}

# def getTranscriptionsFromModel(audio: dict, model_name="medium"):
#     print("Transcribing...", audio['name'])
#     print("Using model:", model_name)
#     model = whisper.load_model(model_name)
#     result = model.transcribe(audio['path'], )
#     pprint(result)
#     return result["text"]


# def on_progress(stream, chunk, bytes_remaining):
#     """Callback function"""
#     total_size = stream.filesize
#     bytes_downloaded = total_size - bytes_remaining
#     pct_completed = bytes_downloaded / total_size * 100
#     print(f"Status: {round(pct_completed, 2)} %")
