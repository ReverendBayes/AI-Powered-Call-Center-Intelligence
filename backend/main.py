# --- FastAPI Application for Call Intelligence Backend ---
# Handles audio and transcript upload, transcribes audio, sends to GPT, returns insights

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import openai
import tempfile
import whisper
import uvicorn
import os
from dotenv import load_dotenv

# --- Load OpenAI API key from .env so we never hardcode secrets ---
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- initialize FastAPI app ---
# this powers the backend server for both upload + insight APIs
app = FastAPI()

# --- enable CORS (important for local frontend testing) ---
# this allows React or Streamlit UIs to make requests to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- load Whisper model once ---
# loading it globally avoids reloading the model every API call
whisper_model = whisper.load_model("base")  # use "base" or "small" to keep memory light

# --- POST route to receive audio + return insights ---
# takes .wav/.mp3 uploads, transcribes, then hits GPT for behavioral analysis
@app.post("/analyze-audio")
async def analyze_audio(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    # run the speech-to-text step
    result = whisper_model.transcribe(tmp_path)
    transcript = result["text"]

    # feed the transcript to GPT to extract intent, tone, churn risk, etc.
    from backend.gpt_analysis import analyze_transcript  # deferred import to avoid circular
    insights = analyze_transcript(transcript)

    # return both the raw transcript and structured output
    return {
        "transcript": transcript,
        "insights": insights
    }

# --- POST route for raw transcript text upload ---
# useful for testing manually or using pre-existing call logs
@app.post("/analyze-text")
async def analyze_text_input(transcript: str = Form(...)):
    from backend.gpt_analysis import analyze_transcript
    insights = analyze_transcript(transcript)
    return {
        "transcript": transcript,
        "insights": insights
    }

# --- GET healthcheck route for testing ---
@app.get("/ping")
def ping():
    return {"status": "ok"}

# --- run locally with uvicorn when this file is the entrypoint ---
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# --- pip install requirements for MacOS ---
# do this once before running anything else
# recommended to run in a virtualenv or conda env
# use --no-deps on keras/tensorflow to avoid Mac Intel crash bugs
#
# pip install openai whisper fastapi python-dotenv uvicorn[standard] torchaudio
# pip install transformers==4.37.2  # lock version for stability
# pip install keras==2.11.0 --no-deps  # avoid Apple Silicon issues if keras is needed downstream
# pip install spacy==3.7.2 presidio-analyzer presidio-anonymizer
# python -m spacy download en_core_web_sm
