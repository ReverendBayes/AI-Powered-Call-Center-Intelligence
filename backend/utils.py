import logging
from transformers import GPT2TokenizerFast

# --- LOGGING SETUP ---
# Use a basic logger for error tracking and debug visibility
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("call-intelligence-utils")

# --- TOKENIZER UTILITY ---
# Used to estimate token counts (e.g., for truncation or model limits)
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

def count_tokens(text):
    # Token counting for text chunking and model prompts
    return len(tokenizer.encode(text))

def safe_truncate(text, max_tokens):
    # Returns a truncated version of the input text within token budget
    tokens = tokenizer.encode(text)
    if len(tokens) <= max_tokens:
        return text
    truncated = tokenizer.decode(tokens[:max_tokens])
    return truncated

def log_exception(context, err):
    # Logs errors with consistent format for traceability
    logger.error(f"[Error in {context}] {str(err)}")
