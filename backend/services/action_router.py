import sys
import os

# Add chatbot_logic to sys.path to import the NLP engine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../chatbot_logic')))
try:
    from chatbot import process_query
except ImportError:
    # Fallback if path is weird
    def process_query(q): return {"intent": "UNKNOWN", "confidence": 0, "entities": {}}

from services.attendance_service import get_overall_attendance, run_absence_projection
from services.timetable_service import get_todays_timetable, get_next_class
from services.fee_service import get_fee_summary, get_fee_deadlines
from services.exam_service import get_upcoming_exams
from services.library_service import search_books
from services.rms_service import create_rms_ticket, check_rms_status
from services.leave_service import apply_leave, get_leave_status
from services.message_service import search_messages
from services.placement_service import get_eligible_drives, register_for_drive
from services.academic_service import get_profile, calculate_target_marks
from services.response_generator import generate_response

def handle_user_query(query: str, registration_number: str) -> str:
    # 1. Pass query to NLP Engine
    nlp_result = process_query(query)
    
    intent = nlp_result['intent']
    entities = nlp_result['entities']
    query_type = nlp_result.get('query_type')
    
    # Needs clarification handles ambiguity
    if nlp_result.get('needs_clarification') or intent == "UNKNOWN":
        return generate_response(intent, nlp_result)
        
    # 2. Route to Business Service based on Intent
    data = {}
    
    try:
        if intent == "GREETING":
            data = {"message": "Hello Verto! How can I assist you with your academic inquiries today?"}
            
        elif intent == "ATTENDANCE":
            data = get_overall_attendance(registration_number)
            
        elif intent == "ATTENDANCE_PROJECTION":
            absent_days = int(entities.get("count", 1))
            subject = entities.get("subject", query) # Fallback to full query
            
            # Check if there is a specific subject mentioned in the query
            from services.attendance_service import run_subject_absence_projection
            
            # Smart Context: If the user is referring to "next class" or "that class", dynamically fetch it!
            query_lower = query.lower()
            if "next class" in query_lower or "that class" in query_lower or "this class" in query_lower:
                nc_data = get_next_class(registration_number)
                if "next_class" in nc_data:
                    subject = nc_data["next_class"]["subject"]
            
            # Simple heuristic: if query contains words like 'class' or specific subject keywords alongside projection keywords
            # For hackathon, we can try subject projection first, and if it fails to find subject, fallback to overall.
            res = run_subject_absence_projection(registration_number, subject, absent_days)
            if "error" in res and "Could not find a subject matching" in res["error"]:
                data = run_absence_projection(registration_number, absent_days)
            else:
                data = res
                data["is_subject_projection"] = True
            
        elif intent == "TIMETABLE":
            # Very basic extraction, real impl would map entities better
            day = entities.get("day")
            data = get_todays_timetable(registration_number, day)
            
        elif intent == "NEXT_CLASS":
            data = get_next_class(registration_number)
            
        elif intent == "FEES":
            data = get_fee_summary(registration_number)
            
        elif intent == "FEE_DEADLINE":
            data = get_fee_deadlines(registration_number)
            
        elif intent == "EXAM":
            data = get_upcoming_exams(registration_number, limit=1)
            
        elif intent == "LIBRARY":
            subject = entities.get("subject", query) # fallback to full query if no subject found
            data = search_books(subject, limit=1)
            
        elif intent == "CREATE_RMS":
            category = entities.get("subject", "General")
            # In a real app we'd ask for description in a multi-turn way
            data = create_rms_ticket(registration_number, category, query)
            
        elif intent == "RMS_STATUS":
            data = check_rms_status(registration_number, limit=1)
            
        elif intent == "HOSTEL_LEAVE":
            # Hardcoded dates for demo purposes
            data = apply_leave(registration_number, "Hostel", "2026-09-01", "2026-09-05", query)
            
        elif intent == "HOSTEL_LEAVE_STATUS":
            data = get_leave_status(registration_number, limit=1)
            
        elif intent == "NOTICES":
            subject = entities.get("subject")
            data = search_messages(subject, limit=1)
            
        elif intent == "PLACEMENT_ELIGIBILITY":
            data = get_eligible_drives(registration_number)
            
        elif intent == "PLACEMENT_REGISTER":
            # For hackathon, just grab the first eligible drive and register
            el_data = get_eligible_drives(registration_number)
            if "eligible_drives" in el_data and el_data["eligible_drives"]:
                drive_id = el_data["eligible_drives"][0]["drive_id"]
                data = register_for_drive(registration_number, drive_id)
            else:
                data = {"error": "You are not eligible for any drives to register for."}
                
        elif intent == "CGPA_CALCULATOR":
            subject = entities.get("subject", "CSE301")
            grade = entities.get("target_grade", "O")
            data = calculate_target_marks(registration_number, subject, grade)
            
        elif intent == "PROFILE":
            data = get_profile(registration_number)
            
        else:
            data = {"error": f"Service for intent '{intent}' is not yet implemented."}
            
    except Exception as e:
        data = {"error": f"Internal Service Error: {str(e)}"}

    # 3. Pass raw data to Response Generator
    return generate_response(intent, data, query_type)
