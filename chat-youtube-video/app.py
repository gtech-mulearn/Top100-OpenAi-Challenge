import streamlit as st
from businessLogic import transcribeVideoOrchestrator



def main():
    st.set_page_config(page_title="Chat Youtube", page_icon="🏖", layout="centered")
    
    st.title("Youtube Video Analyzer")    
    st.write("Get Video Transcription, Video Topics Summary and Video Content Analysis in just one click.")    


    # User input: YouTube URL
    url = st.text_input("Enter YouTube URL:")    
   
    # models = ["tiny", "base", "small", "medium", "large"]

    if st.button("Process Video"):
    
                if url:
                    result = transcribeVideoOrchestrator(url)

                    if result:
                        st.subheader("Content Analysis")
                        st.write(result["analysis"])
                        st.subheader("Points covered:")
                        st.write(result["topics"])
                        st.subheader("Transcription:")
                        st.write(result.get('transcription'))
                    else:
                        st.error("Error occurred while transcribing.")
                        st.write("Please try again.")

    st.markdown('<div style="margin-top: 450px;"</div>',
                unsafe_allow_html=True)


if __name__ == "__main__":
    main()
