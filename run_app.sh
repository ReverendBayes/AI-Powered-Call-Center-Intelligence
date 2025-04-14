#!/bin/bash

# --- run_app.sh ---
# Launches the FastAPI backend on port 8001, then opens the React frontend
# Ideal for quick demos and local testing

# Optional: preload test data (uncomment if needed)
# echo "Loading test data into DuckDB..."
# python analytics/duckdb_loader.py

# Start the FastAPI backend on port 8001
echo "🔁 Starting FastAPI backend on http://localhost:8001 ..."
uvicorn backend.main:app --reload --port 8001 &

# Wait a few seconds to let backend spin up
sleep 2

# Open frontend in default browser
echo "🌐 Opening React frontend..."
open http://localhost:3000

# Helpful reminder
echo "Reminder: In another terminal, start the frontend with:"
echo "cd frontend && npm start"
