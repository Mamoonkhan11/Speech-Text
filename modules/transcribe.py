import streamlit as st
import whisper

@st.cache_resource
def load_model():
    # Load the base Whisper model and can be tiny, base based on accuracy and performance needs
    return whisper.load_model("base")

# All supported languages by Whisper
def transcribe_file(model, file_path: str, language: str):
    lang_map = {
    "Afrikaans": "af", "Albanian": "sq", "Amharic": "am", "Arabic": "ar", "Armenian": "hy",
    "Assamese": "as", "Azerbaijani": "az", "Basque": "eu", "Belarusian": "be", "Bengali": "bn",
    "Bosnian": "bs", "Bulgarian": "bg", "Burmese": "my", "Catalan": "ca", "Chinese": "zh",
    "Croatian": "hr", "Czech": "cs", "Danish": "da", "Dutch": "nl", "English": "en",
    "Estonian": "et", "Finnish": "fi", "French": "fr", "Galician": "gl", "German": "de",
    "Greek": "el", "Gujarati": "gu", "Hebrew": "he", "Hindi": "hi", "Hungarian": "hu",
    "Icelandic": "is", "Indonesian": "id", "Italian": "it", "Japanese": "ja", "Javanese": "jv",
    "Kannada": "kn", "Kazakh": "kk", "Khmer": "km", "Kinyarwanda": "rw", "Korean": "ko",
    "Lao": "lo", "Latin": "la", "Latvian": "lv", "Lithuanian": "lt", "Macedonian": "mk",
    "Malay": "ms", "Malayalam": "ml", "Maltese": "mt", "Maori": "mi", "Marathi": "mr",
    "Mongolian": "mn", "Nepali": "ne", "Norwegian": "no", "Odia": "or", "Pashto": "ps",
    "Persian": "fa", "Polish": "pl", "Portuguese": "pt", "Punjabi": "pa", "Romanian": "ro",
    "Russian": "ru", "Samoan": "sm", "Serbian": "sr", "Sindhi": "sd", "Sinhala": "si",
    "Slovak": "sk", "Slovenian": "sl", "Somali": "so", "Spanish": "es", "Sundanese": "su",
    "Swahili": "sw", "Swedish": "sv", "Tagalog": "tl", "Tamil": "ta", "Telugu": "te",
    "Thai": "th", "Turkish": "tr", "Ukrainian": "uk", "Urdu": "ur", "Uzbek": "uz",
    "Vietnamese": "vi", "Welsh": "cy", "Yiddish": "yi", "Yoruba": "yo", "Zulu": "zu"
}
    code = lang_map.get(language, "en")
    result = model.transcribe(file_path, language=code)
    return result["text"]