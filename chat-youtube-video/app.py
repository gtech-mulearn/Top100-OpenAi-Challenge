import streamlit as st
from businessLogic import transcribeVideoOrchestrator



def main():
    st.set_page_config(page_title="Chat Youtube", page_icon="🏖", layout="centered")
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
    
    st.title("Chat with Video")    
    st.write("Seamlessly converse with videos, receive text responses, and skip watching the lengthy video content.")    


    # User input: YouTube URL
    url = st.text_input("Enter YouTube URL:")    
    # my_upload = st.file_uploader("Upload a video", type=["mp4"])
    # print(my_upload)

    # User input: model
    # models = ["tiny", "base", "small", "medium", "large"]
    # model = st.selectbox("Select Model:", models)
    # st.write(
    
    
    #     "If you take a smaller model it is faster but not as accurate, whereas a larger model is slower but more accurate.")
    with st.sidebar:
        api_key=st.text_input("Enter api key")
    if st.button("Process Video"):
        if my_upload is not None:
            if my_upload.size > MAX_FILE_SIZE:
                st.error("The uploaded file is too large. Please upload an image smaller than 5MB.")
            else:
                print(my_upload)
                # transcribeVideoCustom(my_upload, "whisper-1")
        else:
            if url:
                result = transcribeVideoOrchestrator(url, "tiny")

                if result:
                    st.subheader("Transcription:")
                    st.write(result.get('transcription'))
                    st.subheader("Points covered:")
                    st.write(result["topics"])
                    st.subheader("Content Analysis")
                    st.write(result["analysis"])
                else:
                    st.error("Error occurred while transcribing.")
                    st.write("Please try again.")
    

    st.markdown('<div style="margin-top: 450px;"</div>',
                unsafe_allow_html=True)


if __name__ == "__main__":
    main()
