def init_session_state(st):
    defaults = {
        'sentences': [],
        'is_reading': False,
        'current_sentence': 0,
        'pdf_file': None,
        'autoplay': True,
        'buffer_size': 5,
        'reading_mode': "Full document audio",
        'playback_speed': 1.0
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
