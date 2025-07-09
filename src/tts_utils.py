from gtts import gTTS
import os

def generate_audio(text, filename, lang='en'):
    """Generate audio file from text using gTTS."""
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)
        return True
    except Exception as e:
        print(f"Error generating audio: {e}")
        return False

def estimate_duration(text, words_per_minute=150):
    """Estimate reading duration based on word count."""
    word_count = len(text.split())
    duration_seconds = (word_count / words_per_minute) * 60
    return max(duration_seconds, 1.0)  # Minimum 1 second

def cleanup_audio_files(audio_dir):
    """Clean up temporary audio files."""
    if os.path.exists(audio_dir):
        for file in os.listdir(audio_dir):
            if file.endswith('.mp3'):
                os.remove(os.path.join(audio_dir, file))
