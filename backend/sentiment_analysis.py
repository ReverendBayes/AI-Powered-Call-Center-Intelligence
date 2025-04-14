from transformers import pipeline

# --- SENTIMENT ANALYSIS ---
# This runs a lightweight, fast classifier from HuggingFace (DistilBERT) 
# to tag emotional tone on chunks of transcript text.
#
# It doesn't use GPT Because:
# - This model (DistilBERT) is free and local — no API costs or latency
# - It's fast for batch tagging, good for dashboards and heatmaps
# - It gives clear "POSITIVE", "NEGATIVE", "NEUTRAL" labels with confidence scores
#
# GPT (via gpt_analysis.py) already handles the complex behavioral reasoning.
# This is just here to track tone segment-by-segment for visual timelines.
#
# You can swap this out later with GPT-4o if you want deeper nuance,
# but this is the fast, reliable default.

# --- INIT SENTIMENT PIPELINE ---
# Load pre-trained HuggingFace model for sentiment classification
# Using distilbert-based sentiment model (lightweight + effective)
sentiment_classifier = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    # Break input into chunks to avoid model overload
    # HuggingFace works best on segments, not giant blobs
    segments = split_text_into_chunks(text, max_words=120)

    sentiment_results = []
    for segment in segments:
        # Run model on each chunk
        result = sentiment_classifier(segment)[0]  # get label and score
        sentiment_results.append({
            "text": segment,
            "label": result["label"],
            "score": round(result["score"], 3)
        })

    return sentiment_results

def split_text_into_chunks(text, max_words=120):
    # Split text into chunks with max word count for model stability
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i + max_words])
        chunks.append(chunk.strip())
    return chunks
