from gtts import gTTS
import os

def get_audio_duration(filepath: str, fallback_text: str | None = None, words_per_minute: int = 150) -> float:
    """Return audio duration in seconds using mutagen if available; fallback to estimate.

    If mutagen isn't installed or parsing fails, estimate by words per minute if fallback_text is provided.
    """
    try:
        from mutagen.mp3 import MP3  # type: ignore
        audio = MP3(filepath)
        dur = float(getattr(audio.info, 'length', 0.0))
        if dur and dur > 0:
            return dur
    except Exception:
        pass

    if fallback_text:
        words = len(fallback_text.split())
        return max((words / words_per_minute) * 60.0, 1.0)
    return 1.0

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

def combine_audio_files(audio_dir, output_file):
    """Combine all sentence MP3s in audio_dir into one MP3 file using pydub."""
    from pydub import AudioSegment
    files = sorted([f for f in os.listdir(audio_dir) if f.endswith('.mp3')])
    if not files:
        return False
    combined = AudioSegment.empty()
    for f in files:
        combined += AudioSegment.from_mp3(os.path.join(audio_dir, f))
    combined.export(output_file, format="mp3")
    return True
