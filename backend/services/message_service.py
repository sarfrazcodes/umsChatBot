from models import Message
from extensions import db
from rapidfuzz import fuzz, process

def search_messages(query=None, limit=5):
    all_msgs = Message.query.order_by(Message.published_at.desc()).all()
    
    if not all_msgs:
        return {"message": "No messages found."}
        
    if not query:
        # Return latest messages if no query provided
        recent = all_msgs[:limit]
        return {
            "query": None,
            "results": [
                {
                    "title": m.title,
                    "category": m.category,
                    "content": m.content,
                    "date": m.published_at.strftime("%d %b %Y %H:%M") if m.published_at else None,
                    "department": m.department
                } for m in recent
            ]
        }
        
    # NLP Fuzzy matching based on title and tags
    scored_msgs = []
    for m in all_msgs:
        search_corpus = f"{m.title} {m.tags} {m.category}".lower()
        score = fuzz.token_sort_ratio(query.lower(), search_corpus)
        if score > 30: # Threshold
            scored_msgs.append((m, score))
            
    scored_msgs.sort(key=lambda x: x[1], reverse=True)
    top_results = [m[0] for m in scored_msgs[:limit]]
    
    if not top_results:
        return {"message": f"No messages found matching '{query}'."}
        
    return {
        "query": query,
        "results": [
            {
                "title": m.title,
                "category": m.category,
                "content": m.content,
                "date": m.published_at.strftime("%d %b %Y %H:%M") if m.published_at else None,
                "department": m.department
            } for m in top_results
        ]
    }
