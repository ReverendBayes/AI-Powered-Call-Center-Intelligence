import spacy
from presidio_analyzer import AnalyzerEngine, RecognizerResult
from presidio_anonymizer import AnonymizerEngine
import re

# --- INIT PII DETECTORS ---
# Presidio detects standard entities; spaCy used for token parsing
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()
nlp = spacy.load("en_core_web_sm")

# --- CUSTOM REGEX FOR TELECOM ---
# Account IDs: allowed for supervisor review — do not redact
CUSTOM_PATTERNS = {
    "ACCOUNT_ID": r"\b[0-9]{10,12}\b"
}

# --- DETECT PII ENTITIES ---
# Only redact US_SSN; others are flagged but preserved
REDACT_ENTITIES = ["US_SSN"]

def detect_and_redact(text: str):
    # Run standard Presidio detection
    results: list[RecognizerResult] = analyzer.analyze(
        text=text,
        entities=["PHONE_NUMBER", "EMAIL_ADDRESS", "PERSON", "LOCATION", "DATE_TIME", "US_SSN"],
        language="en"
    )

    # Add any matched account numbers via regex (flagged, not redacted)
    for label, pattern in CUSTOM_PATTERNS.items():
        for match in re.finditer(pattern, text):
            results.append(
                RecognizerResult(
                    entity_type=label,
                    start=match.start(),
                    end=match.end(),
                    score=0.9
                )
            )

    # Apply anonymization only to explicitly redacted entity types
    to_redact = [r for r in results if r.entity_type in REDACT_ENTITIES]
    redacted_text = anonymizer.anonymize(text=text, analyzer_results=to_redact).text

    # Return full PII span metadata
    pii_spans = [
        {
            "entity": r.entity_type,
            "start": r.start,
            "end": r.end,
            "text": text[r.start:r.end]
        } for r in results
    ]

    return {
        "redacted_text": redacted_text,
        "pii_detected": pii_spans
    }
