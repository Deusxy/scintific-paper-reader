import streamlit as st
import streamlit.components.v1 as components
import os
import time
import base64
import tempfile
from src.pdf_utils import extract_text
from src.text_filter import clean_text, split_sentences, analyze_text_quality
from src.tts_utils import generate_audio, estimate_duration, cleanup_audio_files

# Configure Streamlit page
st.set_page_config(
    page_title="NaturalReader Clone",
    page_icon="🗣️",
    layout="wide"
)

# Custom CSS for NaturalReader-like interface
st.markdown("""
<style>
.main-container {
    display: flex;
    height: 100vh;
}

.pdf-viewer {
    border: 2px solid #e0e0e0;
    border-radius: 10px;
    height: 700px;
    overflow: hidden;
    background: #f9f9f9;
}

.reading-panel {
    background: #ffffff;
    border: 2px solid #e0e0e0;
    border-radius: 10px;
    padding: 20px;
    height: 700px;
    overflow-y: auto;
}

.current-sentence {
    background: linear-gradient(90deg, #ffeb3b, #fff59d);
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
    font-size: 18px;
    line-height: 1.6;
    font-weight: 500;
    border-left: 4px solid #f57c00;
    animation: highlight 0.5s ease-in-out;
}

.next-sentence {
    background: #e3f2fd;
    padding: 12px;
    border-radius: 8px;
    margin: 8px 0;
    font-size: 16px;
    line-height: 1.5;
    border-left: 4px solid #2196f3;
}

.previous-sentence {
    background: #f5f5f5;
    padding: 10px;
    border-radius: 8px;
    margin: 5px 0;
    font-size: 14px;
    line-height: 1.4;
    color: #666;
    opacity: 0.7;
}

.control-bar {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    border-radius: 10px;
    margin: 20px 0;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.stats-panel {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
}

.filter-stats {
    background: #e8f5e8;
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
    border-left: 4px solid #4caf50;
}

@keyframes highlight {
    from { transform: scale(0.98); opacity: 0.8; }
    to { transform: scale(1); opacity: 1; }
}

.stButton > button {
    background: linear-gradient(90deg, #667eea, #764ba2);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 10px 20px;
    font-weight: bold;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
</style>
""", unsafe_allow_html=True)

def render_pdf_viewer(pdf_file):
    """Render PDF in iframe like NaturalReader."""
    # Save uploaded file to temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(pdf_file.getvalue())
        tmp_path = tmp_file.name
    
    # Convert to base64 for embedding
    with open(tmp_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    
    # Clean up temp file
    os.unlink(tmp_path)
    
    pdf_display = f'''
    <div class="pdf-viewer">
        <iframe src="data:application/pdf;base64,{base64_pdf}" 
                width="100%" height="100%" 
                style="border: none;">
            <p>Your browser does not support PDFs. 
               <a href="data:application/pdf;base64,{base64_pdf}">Download the PDF</a>.</p>
        </iframe>
    </div>
    '''
    return pdf_display

# Initialize session state
if 'sentences' not in st.session_state:
    st.session_state.sentences = []
if 'is_reading' not in st.session_state:
    st.session_state.is_reading = False
if 'current_sentence' not in st.session_state:
    st.session_state.current_sentence = 0
if 'pdf_file' not in st.session_state:
    st.session_state.pdf_file = None
if 'autoplay' not in st.session_state:
    st.session_state.autoplay = True

# App header
st.markdown("""
<div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; border-radius: 10px; margin-bottom: 30px;">
    <h1>🗣️ NaturalReader Clone</h1>
    <p style="font-size: 18px;">Advanced PDF Reader with Intelligent Text Filtering</p>
</div>
""", unsafe_allow_html=True)

# File upload
uploaded_file = st.file_uploader("📄 Upload a PDF Document", type=["pdf"], 
                                help="Upload a PDF to start reading with intelligent text filtering")

if uploaded_file is not None:
    st.session_state.pdf_file = uploaded_file
    
    # Process PDF with advanced filtering
    with st.spinner("🔍 Processing PDF with advanced text filtering..."):
        try:
            raw_text = extract_text(uploaded_file)
            
            # Choose filter mode
            mode = st.sidebar.radio(
                "Filter Mode",
                options=["balanced", "strict"],
                index=0,
                help="Balanced keeps more sentences; Strict removes brackets, formulas, numeric tables, etc."
            )

            # Analyze text before filtering
            text_stats = analyze_text_quality(raw_text, mode=mode)
            
            # Apply aggressive filtering
            filtered_text = clean_text(raw_text, mode=mode)
            sentences = split_sentences(filtered_text, mode=mode)
            st.session_state.sentences = sentences
            
            # Show filtering results
            st.markdown('<div class="filter-stats">', unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📄 Total Lines", text_stats['total_lines'])
            with col2:
                st.metric("✅ Readable", f"{text_stats['readable_percentage']:.1f}%")
            with col3:
                st.metric("📝 Clean Sentences", len(sentences))
            with col4:
                st.metric("🚫 Filtered Out", text_stats['filtered_out'])
                
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Show what was filtered out
            with st.expander("� See what was filtered out", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"🔗 Brackets removed: {text_stats['brackets_removed']}")
                    st.write(f"🧮 Formulas removed: {text_stats['formulas_removed']}")
                with col2:
                    st.write(f"📋 Headers removed: {text_stats['headers_removed']}")  
                    st.write(f"🌐 URLs removed: {text_stats['urls_removed']}")
            
        except Exception as e:
            st.error(f"❌ Error processing PDF: {e}")

# Main interface - PDF viewer and reading panel
if st.session_state.sentences:
    
    # Control panel
    st.markdown('<div class="control-bar">', unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns([3, 1.2, 1.2, 1.2, 1.2])
    
    with col1:
        st.markdown("### 🎛️ Reading Controls")
    
    with col2:
        # Start from beginning (resets index)
        if st.button("🔊 Start", disabled=st.session_state.is_reading):
            st.session_state.current_sentence = 0
            cleanup_audio_files("audio")
            st.session_state.is_reading = True
    
    with col3:
        # Toggle Pause/Continue
        if st.session_state.is_reading:
            if st.button("⏸️ Pause"):
                st.session_state.is_reading = False
        else:
            if st.button("▶️ Continue", disabled=not st.session_state.sentences):
                st.session_state.is_reading = True
    
    with col4:
        if st.button("⏭️ Next", disabled=st.session_state.current_sentence >= len(st.session_state.sentences) - 1):
            if st.session_state.current_sentence < len(st.session_state.sentences) - 1:
                st.session_state.current_sentence += 1
                st.session_state.is_reading = False  # stop any ongoing playback before manual skip
    
    with col5:
        if st.button("🔄 Reset"):
            st.session_state.is_reading = False
            st.session_state.current_sentence = 0
            cleanup_audio_files("audio")

    # Progress bar
    if st.session_state.sentences:
        progress = st.session_state.current_sentence / len(st.session_state.sentences)
        st.progress(progress)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📍 Position", f"{st.session_state.current_sentence + 1}/{len(st.session_state.sentences)}")
        with col2:
            st.metric("📊 Progress", f"{progress*100:.1f}%")
        with col3:
            st.metric("⏳ Remaining", len(st.session_state.sentences) - st.session_state.current_sentence - 1)

    st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content layout
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### 📖 PDF Document")
        pdf_html = render_pdf_viewer(st.session_state.pdf_file)
        st.markdown(pdf_html, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🎯 Reading Progress")
        st.markdown('<div class="reading-panel">', unsafe_allow_html=True)

        current_idx = st.session_state.current_sentence

        # Always show something meaningful
        if st.session_state.sentences:
            # Previous
            if current_idx > 0:
                prev_sentence = st.session_state.sentences[current_idx - 1]
                st.markdown(f'<div class="previous-sentence">Previous: {prev_sentence}</div>', unsafe_allow_html=True)

            # Current (Now Reading)
            if current_idx < len(st.session_state.sentences):
                current_sentence = st.session_state.sentences[current_idx]
                st.markdown(f'<div class="current-sentence">🎯 Now Reading: {current_sentence}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="current-sentence">🎯 Done</div>', unsafe_allow_html=True)

            # Next
            if current_idx < len(st.session_state.sentences) - 1:
                next_sentence = st.session_state.sentences[current_idx + 1]
                st.markdown(f'<div class="next-sentence">Next: {next_sentence}</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
    
    # Audio playback area
    audio_placeholder = st.empty()

    # Reading logic
    if st.session_state.is_reading and st.session_state.current_sentence < len(st.session_state.sentences):
        current_sentence = st.session_state.sentences[st.session_state.current_sentence]
        
        # Generate and play audio
        if not os.path.exists("audio"):
            os.makedirs("audio")
        
        audio_path = f"audio/sentence_{st.session_state.current_sentence:03}.mp3"
        
        if generate_audio(current_sentence, audio_path):
            # Play the audio
            with audio_placeholder.container():
                idx = st.session_state.current_sentence
                if st.session_state.autoplay:
                    try:
                        with open(audio_path, 'rb') as f:
                            b64 = base64.b64encode(f.read()).decode('utf-8')
                        components.html(
                            f"""
                            <audio controls autoplay onloadeddata='this.currentTime=0; this.play();' preload='auto'>
                                <source src='data:audio/mp3;base64,{b64}' type='audio/mpeg'>
                            </audio>
                            """,
                            height=80,
                        )
                        st.caption("If you don’t hear anything, click Play once to allow audio in your browser.")
                    except Exception:
                        st.audio(audio_path, format='audio/mp3')
                else:
                    st.audio(audio_path, format='audio/mp3')
            
            # Estimate duration and wait
            duration = estimate_duration(current_sentence)
            time.sleep(duration + 1.0)
            
            # Move to next sentence
            st.session_state.current_sentence += 1
            st.rerun()
        else:
            st.error("❌ Failed to generate audio")
            st.session_state.is_reading = False
    
    elif st.session_state.is_reading and st.session_state.current_sentence >= len(st.session_state.sentences):
        # Reading completed
        st.session_state.is_reading = False
        st.success("🎉 Reading completed!")
        st.balloons()

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.info("**Voice:** Google TTS")
    st.info("**Language:** English") 
    st.info("**Quality:** High")
    st.checkbox("Autoplay audio (may need 1st click)", value=st.session_state.autoplay, key='autoplay',
                help="Browsers often block autoplay until you interact (click Start or Play).")
    
    if st.session_state.sentences:
        st.markdown("### 📊 Document Stats")
        st.write(f"**Sentences:** {len(st.session_state.sentences)}")
        total_words = sum(len(s.split()) for s in st.session_state.sentences)
        st.write(f"**Words:** {total_words}")
        est_time = total_words / 150  # 150 WPM
        st.write(f"**Est. Time:** {est_time:.1f} min")
        
        if st.button("🗑️ Clear"):
            for key in ['sentences', 'is_reading', 'current_sentence', 'pdf_file']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

# Footer
st.markdown("---")
st.markdown("**🚀 Advanced NaturalReader Clone** - Intelligent PDF Reading with Aggressive Text Filtering")
