import re
import time

def estimate_word_timings(text, total_duration):
    """Estimate timing for each word in a sentence."""
    words = text.split()
    if not words:
        return []
    
    # Simple estimate: equal time per word
    time_per_word = total_duration / len(words)
    
    timings = []
    current_time = 0
    
    for word in words:
        timings.append({
            'word': word,
            'start_time': current_time,
            'end_time': current_time + time_per_word
        })
        current_time += time_per_word
    
    return timings

def highlight_word_at_time(text, word_timings, current_time):
    """Highlight the word that should be spoken at current_time."""
    words = text.split()
    highlighted_words = []
    
    for i, word in enumerate(words):
        if i < len(word_timings):
            timing = word_timings[i]
            if timing['start_time'] <= current_time <= timing['end_time']:
                highlighted_words.append(f'<mark style="background-color: yellow;">{word}</mark>')
            else:
                highlighted_words.append(word)
        else:
            highlighted_words.append(word)
    
    return ' '.join(highlighted_words)

def create_sentence_highlight(sentence, is_current=False, is_next=False):
    """Create HTML highlight for a sentence."""
    if is_current:
        return f'<div style="background-color: yellow; padding: 10px; border-radius: 5px; margin: 5px 0; font-size: 18px; line-height: 1.6;">{sentence}</div>'
    elif is_next:
        return f'<div style="background-color: #e8f4f8; padding: 10px; border-radius: 5px; margin: 5px 0; font-size: 16px; line-height: 1.6; border-left: 4px solid #2196F3;">{sentence}</div>'
    else:
        return f'<div style="padding: 10px; margin: 5px 0; font-size: 16px; line-height: 1.6; color: #666;">{sentence}</div>'
