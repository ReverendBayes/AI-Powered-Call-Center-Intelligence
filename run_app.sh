#!/bin/bash

# --- run_app.sh ---
# Launches the FastAPI backend using uvicorn, then opens the frontend
# Good for demos, testing, or spinning up locally with one command

# Optional: preload test data via duckdb_loader (uncomment if needed)
# echo "Loading test data into DuckDB..."
# python analytics/duckdb_loader.py

# Start the FastAPI backend
echo "Starting FastAPI backend..."
uvicorn backend.main:app --reload &

# Give the backend a second to boot
sleep 2

# Open the React frontend in default browser
echo "Opening frontend..."
open http://localhost:3000

# Reminder for frontend
echo "Make sure your React app is running in another terminal:"
echo "cd frontend && npm start"