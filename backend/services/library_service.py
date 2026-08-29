from models import LibraryBook
from rapidfuzz import fuzz

def search_books(query, limit=5):
    all_books = LibraryBook.query.all()
    
    if not all_books:
        return {"message": "Library database is empty."}
        
    if not query:
        return {"message": "Please provide a search query (e.g., 'books about stocks' or 'DBMS')."}
        
    scored_books = []
    
    for b in all_books:
        # Create a rich corpus for fuzzy matching
        search_corpus = f"{b.title} {b.author} {b.category} {b.keywords}".lower()
        
        # Calculate a similarity score
        score = fuzz.token_set_ratio(query.lower(), search_corpus)
        
        # We use token_set_ratio here because the query might be "Find DBMS books"
        # and we want "DBMS" to highly match the keywords without being penalized by the word "Find"
        if score > 40:
            scored_books.append((b, score))
            
    # Sort by highest score first
    scored_books.sort(key=lambda x: x[1], reverse=True)
    
    top_results = [b[0] for b in scored_books[:limit]]
    
    if not top_results:
        return {"message": f"Could not find any books matching '{query}' in the library."}
        
    formatted_results = []
    for b in top_results:
        formatted_results.append({
            "title": b.title,
            "author": b.author,
            "category": b.category,
            "availability": "Available" if b.available_copies > 0 else "Out of Stock",
            "available_copies": b.available_copies,
            "total_copies": b.total_copies,
            "location": {
                "building": b.building,
                "floor": b.floor,
                "shelf": b.shelf
            }
        })
        
    return {
        "query": query,
        "results_found": len(formatted_results),
        "books": formatted_results
    }
