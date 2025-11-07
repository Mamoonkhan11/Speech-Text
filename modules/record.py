import time
import tempfile
import sounddevice as sd
import soundfile as sf
import streamlit as st

SAMPLE_RATE = 16000

def start_recording(max_seconds: int):
    st.session_state.recording = True
    st.session_state.start_time = time.time()
    st.session_state._buffer = sd.rec(int(max_seconds * SAMPLE_RATE),
                                      samplerate=SAMPLE_RATE, channels=1, dtype="float32")
    st.rerun()

def stop_recording():
    sd.stop()
    # save wav to temp file
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    sf.write(tmp.name, st.session_state._buffer, SAMPLE_RATE)
    st.session_state.recording = False
    st.session_state.recorded_path = tmp.name