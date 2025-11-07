import streamlit as st

def load_css(path: str):
    with open(path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def header():
    st.markdown("""
    <div class="main-container">
      <h1 class="title">🎙️ SpeakEasy AI</h1>
      <p class="subtitle">Speak or upload your audio to get instant transcription and playback</p>
    </div>
    """, unsafe_allow_html=True)

def mic_glow():
    st.markdown("<div class='mic-wrap'><div class='mic'></div></div>", unsafe_allow_html=True)

import streamlit as st

def segmented_method(options=("Speak", "Upload File"), default="Speak"):

    st.markdown("""
    <style>
    /* Center wrapper for the segmented control */
    .segmented-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 10px;
        margin-bottom: 20px;
    }

    /* Modern dark glass-style background */
    div[data-testid="stSegmentedControl"] {
        background: rgba(20, 25, 35, 0.85);
        border-radius: 12px;
        padding: 6px 8px;
        box-shadow: inset 0 0 10px rgba(0,191,255,0.2);
        max-width: 350px;
        width: 100%;
    }

    /* Each button */
    div[data-testid="stSegmentedControl"] > div {
        color: #b3b8c3 !important;
        font-weight: 500;
        text-align: center;
        transition: all 0.3s ease;
        border-radius: 8px;
    }

    /* Hover effect */
    div[data-testid="stSegmentedControl"] > div:hover {
        background-color: rgba(0,191,255,0.1);
        color: #ffffff !important;
    }

    /* Active selection */
    div[data-testid="stSegmentedControl"] > div[aria-selected="true"] {
        background: linear-gradient(90deg, #00bfff, #0066ff) !important;
        color: #ffffff !important;
        box-shadow: 0 0 10px #00bfff;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="segmented-wrapper">', unsafe_allow_html=True)
        try:
            selected = st.segmented_control(
                "Input Method",
                options=options,
                default=default,
                label_visibility="collapsed"
            )
        except Exception:
            selected = st.radio("🎧 Input Method", options, horizontal=True)
        st.markdown('</div>', unsafe_allow_html=True)
    return selected