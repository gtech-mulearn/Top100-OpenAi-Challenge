from openai import OpenAI
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import validators
from urllib.parse import urlparse, parse_qs

st.set_page_config(page_title="Chat with video", page_icon="🏖", layout="centered")
st.title("Chat with video")
st.write(
    "Seamlessly converse with videos, receive text responses, and skip watching the lengthy video content."
)

client = OpenAI()

st.session_state.setdefault("openai_model", "gpt-3.5-turbo")
st.session_state.setdefault("messages", [])
st.session_state.setdefault("transcription", None)
st.session_state.setdefault("useDefault", False)


def get_video_id(youtube_url):
    # Parse the URL to get the query parameters
    parsed_url = urlparse(youtube_url)
    query_params = parse_qs(parsed_url.query)

    # Extract the video ID from the 'v' parameter
    video_id = query_params.get("v", [""])[0]

    return video_id


def process_video(url):
    with st.spinner("Processing your video.."):
        video_id = get_video_id(url)
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        print(transcript_list)
        transcription = " ".join([entry["text"] for entry in transcript_list])

        st.session_state.transcription = transcription
        st.session_state.messages.clear()
        st.session_state.messages.append(
            {
                "role": "user",
                "content": st.session_state.transcription
                + "This is the transcript of a youtube video. Answer me the following questions based on the video transcript. In your ansewers, use the word video instead of video transcript.",
            }
        )


def get_assistant_response():
    message_placeholder = st.empty()
    full_response = ""
    for response in client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    ):
        full_response += response.choices[0].delta.content or ""
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)
    return full_response

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
    return response.choices[0].message.content

# User input: YouTube URL
defaultValue = "https://www.youtube.com/watch?v=V5GKwuzKQV0"
    
url = st.text_input(label="Enter YouTube URL:", value = defaultValue if st.session_state.useDefault else "")
st.session_state.useDefault = st.checkbox("Use sample Youtube URL")


if st.button("Process Video"):
    if validators.url(url):
        process_video(url)
    else:
        st.warning("Please enter a valid YouTube URL.")


# st.subheader("Topics Covered")
# with st.spinner("Gettings topics"):
#     st.session_state.topics = discoverTopics(st.session_state.transcription)
# st.markdown(st.session_state.topics)

if st.session_state.transcription:
        
    for message in st.session_state.messages[1:]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask anything about the video"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            full_response = get_assistant_response()
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )
