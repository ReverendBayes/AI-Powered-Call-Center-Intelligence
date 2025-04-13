import whisper
import tempfile

# --- INIT MODEL ---
# Load Whisper base model once for fast inference and accuracy balance
model = whisper.load_model("base")

def transcribe_audio(uploaded_file):
    # Save uploaded audio temporarily to disk (Whisper needs a file path)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    # Run transcription — returns full decoded text
    result = model.transcribe(tmp_path)
    transcript = result.get("text", "")

    return transcript