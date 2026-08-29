import re

# Dictionary mapping full names and abbreviations to standard short forms
SUBJECTS_MAP = {
    "dbms": "DBMS",
    "database management": "DBMS",
    "database management systems": "DBMS",
    "dsa": "DSA",
    "data structures": "DSA",
    "data structures and algorithms": "DSA",
    "os": "OS",
    "operating systems": "OS",
    "operating system": "OS",
    "cn": "CN",
    "computer networks": "CN",
    "mathematics": "MATHEMATICS",
    "maths": "MATHEMATICS",
    "math": "MATHEMATICS",
    "python": "PYTHON",
    "java": "JAVA",
    "ai": "AI",
    "artificial intelligence": "AI",
    "ml": "ML",
    "machine learning": "ML"
}

RMS_CATEGORIES = ["ac", "electricity", "internet", "wifi", "fan", "water", "plumbing", "cleaning", "furniture", "light"]

DATES_REGEX = r'\b(today|tomorrow|day after tomorrow|monday|tuesday|wednesday|thursday|friday|saturday|sunday|aaj|kal|\d{1,2}\s+(?:january|february|march|april|may|june|july|august|september|october|november|december)|\d{1,2}/\d{1,2}/\d{2,4})\b'
ROOM_REGEX = r'\b(?:room|block|hall)\s+(\d+[a-zA-Z]?)\b'

def extract_entities(query: str):
    query_lower = query.lower()
    entities = {}

    # Extract Subject using word boundaries and map to standard abbreviation
    for subject_key, standardized_name in SUBJECTS_MAP.items():
        # Escape the key for regex, but handle spaces
        pattern = rf'\b{re.escape(subject_key)}\b'
        if re.search(pattern, query_lower):
            entities['subject'] = standardized_name
            break

    # Extract RMS Category
    for category in RMS_CATEGORIES:
        if re.search(rf'\b{re.escape(category)}\b', query_lower):
            entities['category'] = category.upper()
            break

    # Extract Dates
    date_match = re.search(DATES_REGEX, query_lower)
    if date_match:
        entities['date'] = date_match.group(1)

    # Extract Room
    room_match = re.search(ROOM_REGEX, query_lower)
    if room_match:
        entities['room'] = room_match.group(1)

    return entities

def identify_query_type(query: str, intent: str):
    query_lower = query.lower()
    
    if intent == "ATTENDANCE":
        if "eligible" in query_lower or "eligibility" in query_lower:
            return "ELIGIBILITY"
        
        # Check using word boundaries to prevent 'ai' matching inside 'bhai'
        for subject_key in SUBJECTS_MAP.keys():
            if re.search(rf'\b{re.escape(subject_key)}\b', query_lower):
                return "SUBJECT"
                
        return "OVERALL"
        
    elif intent == "EXAM":
        if "where" in query_lower or "venue" in query_lower or "kaha" in query_lower or "kidhar" in query_lower:
            return "VENUE"
        elif "time" in query_lower:
            return "TIME"
        elif "what" in query_lower and "come" in query_lower:
            return "SYLLABUS" # Though EXAM_SYLLABUS intent should ideally catch this
        else:
            return "DATE"
            
    elif intent == "TIMETABLE":
        if "tomorrow" in query_lower or "kal" in query_lower:
            return "TOMORROW"
        elif "today" in query_lower or "aaj" in query_lower:
            return "TODAY"
        elif re.search(r'\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b', query_lower):
            return "DAY"
        return "FULL"
        
    elif intent == "FEES":
        if "total" in query_lower:
            return "TOTAL"
        elif "deadline" in query_lower or "last date" in query_lower or "kab bharni" in query_lower:
            return "DEADLINE" # Though FEE_DEADLINE should catch this
        return "REMAINING"
        
    elif intent == "FEE_DEADLINE":
        return "DEADLINE"
        
    elif intent == "CREATE_RMS":
        return "CREATE"
    elif intent == "RMS_STATUS":
        return "STATUS"
        
    elif intent == "HOSTEL_INFO":
        return "INFO"
    elif intent == "HOSTEL_LEAVE":
        return "LEAVE"
    elif intent == "HOSTEL_LEAVE_STATUS":
        return "LEAVE_STATUS"

    return None
