from preprocessor import normalize_text
from matcher import match_intent
from entities import extract_entities, identify_query_type
from context import ConversationContext

context_manager = ConversationContext()

def process_query(query: str):
    normalized = normalize_text(query)
    entities = extract_entities(query)
    intent_result = match_intent(normalized)
    
    context_used = False
    
    # Simple Follow-up logic
    query_lower = query.lower()
    has_subject = 'subject' in entities
    word_count = len(query_lower.split())
    is_very_short = word_count <= 3
    
    import re
    # Extract clean words for exact matching
    clean_words = {re.sub(r'[^\w\s]', '', w) for w in query_lower.split()}
    is_follow_up_word = bool(clean_words.intersection({"where", "when", "kab", "kahan", "and"}))
    
    # Only check context if we lack a strong intent OR the query is exceptionally short
    if intent_result['intent'] == "UNKNOWN" or intent_result['confidence'] < 0.65 or is_very_short:
        last_intent = context_manager.last_intent
            
        if last_intent:
            # ONLY inherit context for explicit short follow-ups
            # 1. Very short + has a subject (e.g., "and OS?")
            # 2. Very short + has a follow up keyword (e.g., "where?", "kab?")
            if (is_very_short and has_subject) or (is_very_short and is_follow_up_word):
                intent_result['intent'] = last_intent
                intent_result['needs_clarification'] = False
                intent_result['confidence'] = 0.85 
                context_used = True
                
    # Identify Query Type
    query_type = None
    if intent_result['intent'] != "UNKNOWN":
        query_type = identify_query_type(query, intent_result['intent'])
    
    # Merge context entities if context was used and entity is missing
    if context_used:
        if 'subject' not in entities and context_manager.last_subject:
            entities['subject'] = context_manager.last_subject
            
    # Update Context only if it's a confident new query or a confident follow up
    if intent_result['intent'] != "UNKNOWN":
        context_manager.update(intent_result['intent'], entities)
    
    # Build Exact Final Format
    result = {
        "intent": intent_result['intent'],
        "query_type": query_type,
        "entities": entities,
        "confidence": intent_result['confidence'],
        "alternatives": intent_result.get("alternatives", []),
        "needs_clarification": intent_result['needs_clarification'],
        "context_used": context_used
    }
        
    return result

def run_terminal():
    print("NLP Engine Initialized. Type 'exit' to quit.\n")
    while True:
        try:
            user_input = input("Student: ")
            if user_input.lower() in ['exit', 'quit']:
                break
                
            result = process_query(user_input)
            
            print("\nNLP:")
            print(f"Intent: {result['intent']}")
            if result.get('query_type'):
                print(f"Query Type: {result['query_type']}")
            if result.get('entities'):
                for k, v in result['entities'].items():
                    print(f"Entity: {v} ({k})")
            if result.get('context_used'):
                print(f"Context Used: YES")
            print(f"Confidence: {result['confidence']}")
            
            if result.get('needs_clarification'):
                print("Needs Clarification: YES")
                if result.get('alternatives'):
                    print(f"Alternatives: {result['alternatives']}")
            print("-" * 20 + "\n")
            
        except (KeyboardInterrupt, EOFError):
            break

if __name__ == "__main__":
    run_terminal()
