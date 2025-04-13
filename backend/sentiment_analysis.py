from transformers import pipeline

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