from openai import OpenAI
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import validators
from urllib.parse import urlparse, parse_qs


st.title("Chat with video")
st.write("Seamlessly converse with videos, receive text responses, and skip watching the lengthy video content.")    

client = OpenAI()

st.session_state.setdefault("openai_model", "gpt-3.5-turbo")
st.session_state.setdefault("messages", [])
st.session_state.setdefault("transcription", None)
    

 # User input: YouTube URL
url = st.text_input("Enter YouTube URL:")  

def get_video_id(youtube_url):
    # Parse the URL to get the query parameters
    parsed_url = urlparse(youtube_url)
    query_params = parse_qs(parsed_url.query)

    # Extract the video ID from the 'v' parameter
    video_id = query_params.get('v', [''])[0]

    return video_id

if st.button("Process Video"):
    if validators.url(url):
        with st.status("Processing your video.."):
            video_id = get_video_id(url)
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            transcription = ' '.join([entry['text'] for entry in transcript_list])
            st.session_state.transcription =  transcription
            st.session_state.messages.clear()
            st.session_state.messages.append({"role": "user", "content": st.session_state.transcription + "This is the transcript of a youtube video. Answer me the following questions based on the video transcript. In your ansewers, use the word video instead of video transcript."})
    else:
        st.warning("Please enter a valid YouTube URL.")
        

for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
            
if(st.session_state.transcription):       
    if prompt := st.chat_input("Ask anything about the video"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
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
                    full_response += (response.choices[0].delta.content or "")
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})    
        


