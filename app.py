import streamlit as st
import os
import time
from src.pdf_utils import extract_text
from src.text_filter import clean_text, split_sentences
from src.tts_utils import generate_audio, estimate_duration, cleanup_audio_files

# Configure Streamlit page
st.set_page_config(
    page_title="NaturalReader Clone",
    page_icon="🗣️",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
<style>
.highlight {
    background-color: yellow;
    padding: 10px;
    border-radius: 5px;
    font-size: 18px;
    line-height: 1.6;
    margin: 10px 0;
}
.sentence-container {
    min-height: 100px;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 10px;
    margin: 10px 0;
}
.progress-info {
    font-size: 14px;
    color: #666;
}
</style>
""", unsafe_allow_html=True)

# App title and description
st.title("🗣️ NaturalReader Clone")
st.markdown("Upload a PDF and have it read aloud with sentence highlighting!")

# Initialize session state
if 'sentences' not in st.session_state:
    st.session_state.sentences = []
if 'is_reading' not in st.session_state:
    st.session_state.is_reading = False
if 'current_sentence' not in st.session_state:
    st.session_state.current_sentence = 0

# File upload
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:
    # Process PDF
    with st.spinner("Extracting text from PDF..."):
        try:
            raw_text = extract_text(uploaded_file)
            filtered_text = clean_text(raw_text)
            sentences = split_sentences(filtered_text)
            st.session_state.sentences = sentences
            
            st.success(f"✅ Loaded {len(sentences)} readable sentences")
            
            # Show preview of first few sentences
            st.subheader("Preview:")
            for i, sentence in enumerate(sentences[:3]):
                st.write(f"{i+1}. {sentence}")
            if len(sentences) > 3:
                st.write(f"... and {len(sentences) - 3} more sentences")
                
        except Exception as e:
            st.error(f"Error processing PDF: {e}")

# Reading controls
if st.session_state.sentences:
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🔊 Start Reading", disabled=st.session_state.is_reading):
            st.session_state.is_reading = True
            st.session_state.current_sentence = 0
            # Clean up old audio files
            cleanup_audio_files("audio")
    
    with col2:
        if st.button("⏸️ Stop Reading"):
            st.session_state.is_reading = False
    
    with col3:
        if st.button("🔄 Reset"):
            st.session_state.is_reading = False
            st.session_state.current_sentence = 0
            cleanup_audio_files("audio")

    # Reading progress
    if st.session_state.sentences:
        progress = st.session_state.current_sentence / len(st.session_state.sentences)
        st.progress(progress)
        st.markdown(f'<div class="progress-info">Progress: {st.session_state.current_sentence}/{len(st.session_state.sentences)} sentences</div>', unsafe_allow_html=True)

    # Current sentence display
    sentence_placeholder = st.empty()
    audio_placeholder = st.empty()

    # Reading logic
    if st.session_state.is_reading and st.session_state.current_sentence < len(st.session_state.sentences):
        current_sentence = st.session_state.sentences[st.session_state.current_sentence]
        
        # Display highlighted sentence
        with sentence_placeholder.container():
            st.markdown(f'<div class="sentence-container"><div class="highlight">{current_sentence}</div></div>', unsafe_allow_html=True)
        
        # Generate and play audio
        if not os.path.exists("audio"):
            os.makedirs("audio")
        
        audio_path = f"audio/sentence_{st.session_state.current_sentence:03}.mp3"
        
        if generate_audio(current_sentence, audio_path):
            # Play the audio
            with audio_placeholder.container():
                st.audio(audio_path, format='audio/mp3')
            
            # Estimate duration and wait
            duration = estimate_duration(current_sentence)
            time.sleep(duration + 0.5)  # Add small buffer
            
            # Move to next sentence
            st.session_state.current_sentence += 1
            st.rerun()
        else:
            st.error("Failed to generate audio for current sentence")
            st.session_state.is_reading = False
    
    elif st.session_state.is_reading and st.session_state.current_sentence >= len(st.session_state.sentences):
        # Reading completed
        st.session_state.is_reading = False
        st.success("🎉 Reading completed!")
        cleanup_audio_files("audio")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit, gTTS, and PyMuPDF")
