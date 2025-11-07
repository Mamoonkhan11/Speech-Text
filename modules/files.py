import os
import tempfile

def save_upload_to_tmp(upload):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(upload.name)[-1] or ".wav")
    tmp.write(upload.read())
    return tmp.name

def delete_file(path):
    try:
        if path and os.path.exists(path):
            os.remove(path)
    except Exception:
        pass

def build_report(meta: dict, text: str):
    report = (
        "--- Speech-to-Text Transcription Report ---\n\n"
        f"🕒 Date & Time: {meta['timestamp']}\n"
        f"🌐 Language: {meta['language']}\n"
        f"🎧 Input Method: {meta['method']}\n"
        "---------------------------------------------\n\n"
        f"{text}\n"
    )
    safe_ts = meta["timestamp"].replace(":", "-").replace(" ", "_")
    fname = f"transcription_{meta['language']}_{meta['method'].replace(' ', '_')}_{safe_ts}.txt"
    return report, fname