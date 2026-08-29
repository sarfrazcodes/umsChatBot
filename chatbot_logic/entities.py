import re

# Dictionary mapping full names and abbreviations to standard short forms
SUBJECTS_MAP = {
    # OS - CSE316
    "os": "CSE316",
    "operating systems": "CSE316",
    "operating system": "CSE316",
    "cse316": "CSE316",
    
    # Full Stack - INT221
    "web dev": "INT221",
    "full stack": "INT221",
    "full stack web dev": "INT221",
    "int221": "INT221",
    
    # AI & ML - CSE320
    "ai & ml": "CSE320",
    "machine learning": "CSE320",
    "artificial intelligence": "CSE320",
    "ai": "CSE320",
    "ml": "CSE320",
    "cse320": "CSE320",
    
    # Maths - MTH302
    "maths": "MTH302",
    "mathematics": "MTH302",
    "engineering mathematics": "MTH302",
    "mth302": "MTH302",
    
    # English - PEL136
    "english": "PEL136",
    "english advance": "PEL136",
    "pel136": "PEL136",
    
    # DSA - CSE205
    "dsa": "CSE205",
    "data structures": "CSE205",
    "data structures and algorithms": "CSE205",
    "cse205": "CSE205",
    
    # OOP - INT205
    "oop": "INT205",
    "oops": "INT205",
    "object oriented programming": "INT205",
    "int205": "INT205",
    
    # AI ML Foundation - CSE276
    "ai foundation": "CSE276",
    "ai & ml foundation": "CSE276",
    "cse276": "CSE276",
    
    # CN - CSE306
    "cn": "CSE306",
    "computer networks": "CSE306",
    "cse306": "CSE306",
    
    # Legacy fallbacks
    "dbms": "CSE316",
    "java": "INT205",
    "python": "CSE320"
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

    # Extract Target Grade
    # Match phrases like "O grade", "A+ grade", "9 cgpa", etc.
    grade_match = re.search(r'\b(o|a\+|a|b\+|b|c|d|e|f)\s*grade\b', query_lower)
    if grade_match:
        entities['target_grade'] = grade_match.group(1).upper()
    else:
        cgpa_match = re.search(r'\b(10|9|8|7|6|5)\s*cgpa\b', query_lower)
        if cgpa_match:
            val = cgpa_match.group(1)
            # Map cgpa approx to grade
            cgpa_map = {"10": "O", "9": "A+", "8": "A", "7": "B+", "6": "B", "5": "C"}
            entities['target_grade'] = cgpa_map.get(val, "A")

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
