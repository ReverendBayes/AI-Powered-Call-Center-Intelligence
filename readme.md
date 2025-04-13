# AI-Powered Call Center Intelligence

A full-stack, local-first behavioral intelligence engine for telecom support calls.

Combining Whisper transcription, GPT-4o insights, PII redaction, and visual analytics — this project gives supervisors real-time understanding of what customers feel, need, and signal during calls.

---

## ✅ Use This If You Need:

- Real-time speech-to-text pipelines that actually work
- Churn risk, emotional escalation, and issue classification — extracted live
- Upload audio **or** raw transcripts, get clean insights
- Resolution tactic suggestions tailored by behavioral trajectory
- Open architecture — no Azure, no Power BI
- UI designed to be *user-mesmerizing*, built with **React + TypeScript**

---

## 🔍 What It Does

1. **Transcribes** calls with OpenAI Whisper
2. **Redacts** PII with spaCy + Presidio
3. **Analyzes** behavior with GPT-4o Mini (custom telecom_prompt)
4. **Detects** sentiment with HuggingFace models
5. **Visualizes** post-call trends via DuckDB + Altair
6. **Delivers** results in-browser with a fast, styled React frontend

---

## 🏛️ Architecture

```bash
AI-Powered-Call-Center-Intelligence/
├── backend/                # Core logic: FastAPI, Whisper, GPT, redaction
│   ├── main.py             # FastAPI app entrypoint
│   ├── whisper_transcribe.py
│   ├── pii_redaction.py
│   ├── gpt_analysis.py
│   ├── sentiment_analysis.py
│   ├── utils.py
│   └── models/
│       ├── telecom_prompt.txt
│       ├── system_prompt.txt
│       └── pii_labels.yaml
│
├── frontend/               # React frontend (create-react-app + TypeScript)
│   ├── public/
│   └── src/
│       ├── App.tsx
│       ├── TextUpload.tsx
│       └── App.css
│
├── analytics/              # Post-call analytics and dashboards
│   ├── call_summary.db
│   ├── duckdb_loader.py
│   ├── analysis_notebook.ipynb
│   └── powerdash_components.py
│
├── data/                   # Sample data files
│   ├── transcript.json
│   ├── pii_output.json
│   ├── gpt_output.json
│   └── audio_sample.wav
│
├── config/                 # Configs and environment settings
│   └── settings.yaml
│
├── tests/                  # Unit tests for pipelines
│   ├── test_transcribe.py
│   ├── test_gpt_prompt.py
│   └── test_redaction.py
│
├── .env                    # Local OpenAI API keys (never commit)
├── .gitignore
├── run_app.sh              # CLI launcher for backend
├── requirements.txt
└── README.md
```

---

## ✨ Features

- Upload audio or text — get structured insights
- Emotional arc detection (e.g., Calm → Angry)
- Tactic recommendation engine using structured GPT prompting
- PII masking that preserves useful metadata (e.g. phone/account)
- Sentiment over time + issue heatmaps in notebook
- Fully local: no cloud services required

---

## 🧠 Prompt Logic (telecom_prompt)

```
Analyze the following telecom customer service call and extract:

1. Core issue reported by the customer
2. Classification: Billing, Connectivity, Retention, Inquiry, Cancel
3. Agent resolution steps taken
4. Customer satisfaction at end
5. Was follow-up promised?
6. List any PII mentioned
7. Emotional tone progression (e.g. Calm → Angry)
8. Recommended resolution tactic:
   - Early empathy and follow-up
   - Quick fix and firm response
   - Monitor for volatility
   - Intervene pre-escalation
   - Offer benefit or apology credit
```

---

## ⚡ Live UI (localhost)

- Built with React + TypeScript, styled to match React.dev
- Upload panel: audio file → transcript → insights
- Text panel: paste a transcript → get analysis
- Outputs display with JSON structure and preformatted blocks

---

## 📊 Post-Call Analytics

- Notebook powered by DuckDB + Altair
- In-memory or persistent call storage
- Charts include:
  - Emotional progression
  - Resolution tactic frequency
  - Satisfaction distribution
  - Issue heatmap

---

## 🧩 No Azure or Power BI Required

This is a **standalone**, open-source version of Microsoft’s call intelligence accelerator:

- Uses Whisper + GPT-4o from OpenAI
- All redaction and classification handled locally
- No subscriptions, no vendor lock-in

---

## ⛓ Requirements

Python 3.9+
```bash
pip install -r requirements.txt
```

Add `.env`:
```bash
OPENAI_API_KEY=sk-xxxxx
```

---

## 🚀 Run the App

```bash
./run_app.sh
```

Then visit: [http://localhost:3000](http://localhost:3000)

---

## 📝 License

MIT © 2025