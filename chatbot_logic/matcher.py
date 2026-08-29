import json
import os
from rapidfuzz import fuzz, process
from preprocessor import normalize_text

INTENTS_FILE = os.path.join(os.path.dirname(__file__), "intents.json")

# Configurable Thresholds
CONFIDENCE_THRESHOLD = 0.60
HIGH_CONFIDENCE = 0.75
AMBIGUITY_MARGIN = 0.05

def load_intents():
    with open(INTENTS_FILE, "r") as f:
        raw_intents = json.load(f).get("intents", {})
    
    normalized_intents = {}
    for intent, examples in raw_intents.items():
        normalized_intents[intent] = [normalize_text(ex) for ex in examples]
    return normalized_intents

INTENTS = load_intents()

def match_intent(normalized_query: str):
    if not normalized_query.strip():
        return {
            "intent": "UNKNOWN",
            "confidence": 0.0,
            "needs_clarification": True,
            "alternatives": []
        }

    best_intents = []

    for intent, examples in INTENTS.items():
        # token_sort_ratio provides high accuracy while ignoring word order,
        # but preventing subset false positives that token_set_ratio suffers from.
        match = process.extractOne(normalized_query, examples, scorer=fuzz.token_sort_ratio)
        if match:
            best_intents.append((intent, match[1] / 100.0))

    best_intents.sort(key=lambda x: x[1], reverse=True)

    if not best_intents:
        return {
            "intent": "UNKNOWN",
            "confidence": 0.0,
            "needs_clarification": True,
            "alternatives": []
        }

    top_intent, top_score = best_intents[0]

    # Threshold Check
    if top_score < CONFIDENCE_THRESHOLD:
        return {
            "intent": "UNKNOWN",
            "confidence": round(top_score, 2),
            "needs_clarification": True,
            "alternatives": []
        }

    result = {
        "intent": top_intent,
        "confidence": round(top_score, 2),
        "needs_clarification": False,
        "alternatives": []
    }

    # Top-2 Ambiguity Check
    if len(best_intents) > 1:
        second_intent, second_score = best_intents[1]
        
        # If second score is very close to top score, flag as ambiguous
        if second_score >= CONFIDENCE_THRESHOLD and (top_score - second_score) <= AMBIGUITY_MARGIN:
            result["intent"] = "UNKNOWN"
            result["needs_clarification"] = True
            result["alternatives"] = [
                [top_intent, round(top_score, 2)],
                [second_intent, round(second_score, 2)]
            ]

    return result
