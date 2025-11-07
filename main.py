# Main application file for speakEasy AI - a Streamlit app for audio transcription using Whisper model.

import time
from io import BytesIO
from datetime import datetime
import streamlit as st
from modules.ui import load_css, header, mic_glow, segmented_method
from modules.record import start_recording, stop_recording, SAMPLE_RATE
from modules.transcribe import load_model, transcribe_file
from modules.files import save_upload_to_tmp, delete_file, build_report

# Streamlit page config and CSS
st.set_page_config(page_title="speakEasy AI", page_icon="🎙️", layout="centered")
load_css("assets/styles.css")

# Load Whisper model
model = load_model()

# Initialize session state variables
for k, v in {
    "recording": False,
    "recorded_path": None,
    "start_time": None,
    "text": None,
    "meta": None,
}.items():
    st.session_state.setdefault(k, v)

# UI Header
header()

# Language selection
language = st.selectbox(
    "🌐 Choose Language",
    sorted([
        "Afrikaans", "Albanian", "Amharic", "Arabic", "Armenian", "Assamese", "Azerbaijani",
        "Bashkir", "Basque", "Belarusian", "Bengali", "Bosnian", "Bulgarian", "Burmese",
        "Catalan", "Chinese", "Croatian", "Czech", "Danish", "Dutch", "English", "Estonian",
        "Finnish", "French", "Galician", "Georgian", "German", "Greek", "Gujarati", "Haitian Creole",
        "Hausa", "Hawaiian", "Hebrew", "Hindi", "Hungarian", "Icelandic", "Indonesian", "Italian",
        "Japanese", "Javanese", "Kannada", "Kazakh", "Khmer", "Kinyarwanda", "Korean", "Lao",
        "Latin", "Latvian", "Lithuanian", "Luxembourgish", "Macedonian", "Malagasy", "Malay",
        "Malayalam", "Maltese", "Maori", "Marathi", "Mongolian", "Nepali", "Norwegian", "Odia",
        "Pashto", "Persian", "Polish", "Portuguese", "Punjabi", "Romanian", "Russian", "Samoan",
        "Serbian", "Shona", "Sindhi", "Sinhala", "Slovak", "Slovenian", "Somali", "Spanish",
        "Sundanese", "Swahili", "Swedish", "Tagalog", "Tajik", "Tamil", "Tatar", "Telugu",
        "Thai", "Turkish", "Ukrainian", "Urdu", "Uzbek", "Vietnamese", "Welsh", "Xhosa",
        "Yiddish", "Yoruba", "Zulu"
    ])
)
# MODERN input selector (Streamlit segmented control)
input_method = segmented_method(options=["Speak", "Upload File"], default="Speak")

# SPEAK ───────────────────────────────────────────────────────────────────────
if input_method == "Speak":
    mic_glow()
    max_sec = st.slider("Set Maximum Duration (seconds)", 3, 30, 10)

    if not st.session_state.recording and not st.session_state.recorded_path:
        if st.button(" Start Recording"):
            start_recording(max_sec)

    elif st.session_state.recording:
        elapsed = int(time.time() - st.session_state.start_time)
        st.markdown(f"<p class='timer'>⏱ Recording: {elapsed}s</p>", unsafe_allow_html=True)
        if st.button(" Stop Recording"):
            stop_recording()
            st.success(" Recording saved.")
            st.rerun()

    elif st.session_state.recorded_path:
        st.audio(st.session_state.recorded_path, format="audio/wav")

        c1, c2 = st.columns(2)
        with c1:
            if st.button(" Transcribe Audio"):
                with st.spinner("Transcribing..."):
                    text = transcribe_file(model, st.session_state.recorded_path, language)
                st.session_state.text = text
                st.session_state.meta = {
                    "method": "Microphone Recording",
                    "language": language,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                st.rerun()
        with c2:
            if st.button(" Re-record"):
                delete_file(st.session_state.recorded_path)
                st.session_state.update({"recorded_path": None, "text": None, "meta": None})
                st.rerun()

    # show transcript + download
    if st.session_state.text:
        st.text_area(" Transcribed Text", st.session_state.text, height=220)
        report, fname = build_report(st.session_state.meta, st.session_state.text)
        st.download_button(" Download Transcription Report (.txt)",
                           data=BytesIO(report.encode("utf-8")),
                           file_name=fname, mime="text/plain")
# UPLOAD FILE ────────────────────────────────────────────────────────────────
else:
    up = st.file_uploader(" Upload an audio file", type=["wav", "mp3", "m4a"])
    if up:
        tmp = save_upload_to_tmp(up)
        st.audio(tmp, format="audio/wav")
        if st.button(" Transcribe Uploaded File"):
            with st.spinner("Transcribing..."):
                text = transcribe_file(model, tmp, language)
            st.session_state.text = text
            st.session_state.meta = {
                "method": "File Upload",
                "language": language,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            st.rerun()

    if st.session_state.text:
        st.text_area(" Transcribed Text", st.session_state.text, height=220)
        report, fname = build_report(st.session_state.meta, st.session_state.text)
        st.download_button(" Download Transcription Report (.txt)",
                           data=BytesIO(report.encode("utf-8")),
                           file_name=fname, mime="text/plain")