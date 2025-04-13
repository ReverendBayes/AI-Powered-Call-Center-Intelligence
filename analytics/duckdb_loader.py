# --- duckdb_loader.py ---
# Loads outputs (transcript, redactions, GPT insights) into DuckDB
# Enables SQL queries, charting, and dashboard use

import duckdb
import os
import json
from pathlib import Path

# --- Create or connect to local DuckDB file ---
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)
db_path = data_dir / "call_summary.db"
con = duckdb.connect(str(db_path))

# --- Create table if not exists ---
con.execute("""
CREATE TABLE IF NOT EXISTS calls (
    call_id VARCHAR,
    transcript TEXT,
    redacted_transcript TEXT,
    insights JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# --- Ingest a full call package (transcript + redacted + insights) ---
def load_call_summary(call_id: str, transcript_path: str, redacted_path: str, insights_path: str):
    with open(transcript_path) as f:
        transcript = json.load(f)["text"]  # assume Whisper output format

    with open(redacted_path) as f:
        redacted_transcript = json.load(f)["redacted_text"]

    with open(insights_path) as f:
        insights = json.load(f)  # full structured GPT output

    con.execute("""
        INSERT INTO calls (call_id, transcript, redacted_transcript, insights)
        VALUES (?, ?, ?, ?)
    """, (call_id, transcript, redacted_transcript, json.dumps(insights)))

    print(f"✅ Loaded call_id={call_id} into DuckDB")

# --- Optional query helper for Jupyter notebooks ---
def query(sql: str):
    return con.execute(sql).df()