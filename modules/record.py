# Module for audio recording functionality in SpeakEasy AI Streamlit application.

import streamlit as st

try:
    import sounddevice as sd
    import soundfile as sf
    import tempfile
    import time
    SOUND_ENABLED = True
except Exception:
    SOUND_ENABLED = False

SAMPLE_RATE = 16000

def start_recording(max_seconds: int):
    if not SOUND_ENABLED:
        st.error(" Microphone recording is not supported in this environment.")
        return
    st.session_state.recording = True
    st.session_state.start_time = time.time()
    st.session_state._buffer = sd.rec(
        int(max_seconds * SAMPLE_RATE),
        samplerate=SAMPLE_RATE, channels=1, dtype="float32"
    )
    st.rerun()

def stop_recording():
    if not SOUND_ENABLED:
        return
    sd.stop()
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    sf.write(tmp.name, st.session_state._buffer, SAMPLE_RATE)
    st.session_state.recording = False
    st.session_state.recorded_path = tmp.name
