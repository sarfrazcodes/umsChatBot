import re

# Hinglish keyword mapping
HINGLISH_MAP = {
    "kab": "when",
    "kitni": "how much",
    "batao": "tell",
    "dikhao": "show",
    "meri": "my",
    "mera": "my",
    "ka": "of",
    "ki": "of",
    "chahiye": "need",
    "lagani": "apply",
    "kya": "what",
    "kahan": "where",
    "konsi": "which",
    "konsa": "which",
    "hai": "is",
    "hain": "are",
    "kal": "tomorrow",
    "aaj": "today",
    "abhi": "now"
}

# Words that should NEVER be removed as they completely change meaning
IMPORTANT_WORDS = {
    "not", "no", "tomorrow", "today", "my", "your", "when", "where", "how", 
    "what", "why", "who", "which", "is", "are", "am"
}

# Basic generic stopwords to remove
STOPWORDS = {
    "a", "an", "the", "in", "on", "at", "to", "for", "with", "about", 
    "please", "can", "you", "i", "me", "do", "does", "did", "will", "would"
}

def normalize_text(text: str) -> str:
    # Lowercase
    text = text.lower()
    
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    
    # Tokenize (simple split)
    tokens = text.split()
    
    normalized_tokens = []
    for t in tokens:
        # Translate hinglish words if present
        t = HINGLISH_MAP.get(t, t)
        
        # Keep if important, or if not in simple stopwords
        if t in IMPORTANT_WORDS or t not in STOPWORDS:
            normalized_tokens.append(t)
            
    return " ".join(normalized_tokens)
