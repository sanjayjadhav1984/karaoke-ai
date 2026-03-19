import streamlit as st
from audio_separator.separator import Separator
import os

st.set_page_config(page_title="Karaoke AI", layout="centered")
st.title("🎤 Karaoke Creator AI")
st.write("Upload a song to isolate the instrumental track.")

uploaded_file = st.file_uploader("Choose an MP3/WAV file", type=["mp3", "wav"])

if uploaded_file is not None:
    input_path = "input.mp3"
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.info("Processing... This takes about 30-60 seconds.")
    
    try:
        separator = Separator()
        separator.load_model('UVR-MDX-NET-Voc_FT')
        output_files = separator.separate(input_path)
        
        # Audio-Separator typically returns [instrumental, vocals]
        instrumental_path = output_files[0]
        
        st.success("Done!")
        st.subheader("Your Karaoke Track")
        st.audio(instrumental_path)
        
        with open(instrumental_path, "rb") as file:
            st.download_button(
                label="Download Instrumental",
                data=file,
                file_name="karaoke_track.mp3",
                mime="audio/mpeg"
            )
    except Exception as e:
        st.error(f"Error during processing: {e}")
