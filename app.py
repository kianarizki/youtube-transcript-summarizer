import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""You are YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. 

IMPORTANT: Please provide the summary in the SAME LANGUAGE as the transcript text.
Detect the language automatically and respond in that language.

Please provide the summary of the text given here:  """

# getting the transcript data from the youtube video
def extract_transcript_details(youtube_video_url):
    try:
        # Extract video ID from various youtube video
        if "v=" in youtube_video_url:
            video_id =  youtube_video_url.split("v=")[1].split("&")[0]
        elif "youtube.be/" in youtube_video_url:
            video_id = youtube_video_url.split("youtube.be/")[1].split("?")[0]
        else:
            raise ValueError("Invalid YouTube URL format")

        # First try to get transcript in any available language
        try:
            # Get list of available transcripts
            transcript_list = YouTubeTranscriptApi().list(video_id)

            # try to get transcript in any available language
            transcript_obj = transcript_list.find_transcript(['id', 'en', 'es', 'fr', 'de', 'pt', 'it', 'ru', 'ja', 'ko', 'zh', 'ar'])
            transcript_obj = transcript_obj.fetch()
        
        except:
            # Fallback: try to get any available transcript
            transcript_list = YouTubeTranscriptApi().list(video_id)
            available_transcripts = transcript_list.find_manually_created_transcript(['id', 'en'])
            transcript_obj =  available_transcripts.fetch()
        
        transcript = ""
        for snippet in transcript_obj.snippets:
            transcript += " " + snippet.text

        # Add language info to transcript
        language_info = f"[Language: {transcript_obj.language_code}]\n\n"
        return language_info + transcript

    except Exception as e:
        st.error(f"Error extracting transcript: {str(e)}")
        return None

def generate_gemini_content(transcript_text, prompt):
    model=genai.GenerativeModel("gemini-2.0-flash-001")
    response=model.generate_content(prompt+transcript_text)
    return response.text

def main():
    """Main function to run the Streamlit app"""
    st.title("Youtube Video Transcript Summarizer")
    st.markdown("Enter a YouTube video URL to get AI-powered summary using Gemini")
    youtube_video_url = st.text_input("Enter the Youtube video URL", placeholder="https://www.youtube.com/watch?v=...")

    if youtube_video_url:
        try:
            # Extract video ID for thumbnail
            if "v=" in youtube_video_url:
                video_id = youtube_video_url.split("v=")[1].split("&")[0]
            elif "youtube.be/" in youtube_video_url:
                video_id = youtube_video_url.split("youtube.be/")[1].split("?")[0]
            else:
                video_id = None

            if video_id:
                st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", width='stretch')
        
        except:
            st.warning("Could not display video thumbnail")
        
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Show Raw Transcript"):
            if not youtube_video_url:
                st.warning("Please enter a YouTube URL")
            else:
                with st.spinner("Extracting transcript..."):
                    transcript_text = extract_transcript_details(youtube_video_url)
                    if transcript_text:
                        # Extract language info from transcript
                        if transcript_text.startswith("[Language]"):
                            language_line = transcript_text.split("\n")[0]
                            actual_transcript = "\n".join(transcript_text.split("\n")[2:])
                            st.markdown(f"##Raw Transcript ({language_line})")
                            st.text_area(f"Transcript", actual_transcript, height=400)
                        else:
                            st.markdown("## Raw Transcript:")
                            st.text_area("Transcript", transcript_text, height=400)

                        st.download_button(
                            label="Download Transcript",
                            data=transcript_text,
                            file_name=f"transcript.txt",
                            mime="text/plain"
                        )
                    else:
                        st.error("Failed to extract transcript. Please check if the video has captions available.")
    
    with col2:
        if st.button("Show Summary"):
            if not youtube_video_url:
                st.warning("Please enter a YouTube URL")
            else:
                with st.spinner("Extracting transcript and generating summary..."):
                    transcript_text = extract_transcript_details(youtube_video_url)
                    if transcript_text:
                        summary = generate_gemini_content(transcript_text, prompt)
                        st.markdown("### Summary:")
                        st.write(summary)
                    else:
                        st.error("Failed to extract transcript. Please check if the video has captions available.")

if __name__ == "__main__":
    main()



