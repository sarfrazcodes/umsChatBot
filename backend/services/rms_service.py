from models import RMSRequest, RMSCategory, Student
from extensions import db
from rapidfuzz import fuzz

def get_student_id_by_reg_no(registration_number):
    student = Student.query.filter_by(registration_number=registration_number).first()
    return student.student_id if student else None

def map_category_string_to_id(category_name):
    # Retrieve all categories
    categories = RMSCategory.query.all()
    if not categories:
        return None
        
    # Use NLP fuzzy matching to find the closest category
    best_match = None
    highest_score = 0
    
    for c in categories:
        score = fuzz.token_sort_ratio(category_name.lower(), c.name.lower())
        if score > highest_score:
            highest_score = score
            best_match = c.id
            
    # If confidence is too low, we might want to return a generic 'Other' category or None
    if highest_score > 40:
        return best_match
    return None

def create_rms_ticket(registration_number, category_name, description):
    student_id = get_student_id_by_reg_no(registration_number)
    if not student_id:
        return {"error": "Student not found"}
        
    category_id = map_category_string_to_id(category_name)
    
    # If the database has no categories yet, we can't create it because of FK constraints.
    # In a real app we'd handle this cleanly. For now, we'll return an error.
    if not category_id:
        return {"error": f"Could not map '{category_name}' to a valid RMS category. Please try again."}
        
    ticket = RMSRequest(
        student_id=student_id,
        category_id=category_id,
        description=description,
        status="Open"
    )
    
    db.session.add(ticket)
    db.session.commit()
    
    category = RMSCategory.query.get(category_id)
    
    return {
        "message": f"Successfully created RMS ticket under category '{category.name}'.",
        "ticket_id": ticket.id,
        "status": ticket.status
    }

def check_rms_status(registration_number, ticket_id=None, limit=5):
    student_id = get_student_id_by_reg_no(registration_number)
    if not student_id:
        return {"error": "Student not found"}
        
    if ticket_id:
        ticket = RMSRequest.query.filter_by(student_id=student_id, id=ticket_id).first()
        if not ticket:
            return {"error": f"Ticket #{ticket_id} not found for your account."}
            
        category = RMSCategory.query.get(ticket.category_id)
        return {
            "ticket_id": ticket.id,
            "category": category.name if category else "Unknown",
            "description": ticket.description,
            "status": ticket.status
        }
        
    # Get recent tickets
    tickets = RMSRequest.query.filter_by(student_id=student_id).order_by(RMSRequest.id.desc()).limit(limit).all()
    if not tickets:
        return {"message": "You have no active RMS tickets."}
        
    history = []
    for t in tickets:
        category = RMSCategory.query.get(t.category_id)
        history.append({
            "ticket_id": t.id,
            "category": category.name if category else "Unknown",
            "status": t.status
        })
        
    return {
        "total_tickets": len(history),
        "tickets": history
    }
