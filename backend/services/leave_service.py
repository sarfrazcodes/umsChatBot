from models import Leave, Student
from extensions import db
from datetime import datetime

def get_student_id_by_reg_no(registration_number):
    student = Student.query.filter_by(registration_number=registration_number).first()
    return student.student_id if student else None

def apply_leave(registration_number, leave_type, from_date_str, to_date_str, reason):
    student_id = get_student_id_by_reg_no(registration_number)
    if not student_id:
        return {"error": "Student not found"}
        
    try:
        from_date = datetime.strptime(from_date_str, "%Y-%m-%d").date()
        to_date = datetime.strptime(to_date_str, "%Y-%m-%d").date()
    except ValueError:
        return {"error": "Dates must be in YYYY-MM-DD format."}
        
    if to_date < from_date:
        return {"error": "to_date cannot be earlier than from_date."}
        
    leave = Leave(
        student_id=student_id,
        type=leave_type,
        from_date=from_date,
        to_date=to_date,
        reason=reason,
        status="Pending"
    )
    
    db.session.add(leave)
    db.session.commit()
    
    return {
        "message": f"Successfully applied for {leave_type} leave from {from_date_str} to {to_date_str}.",
        "leave_id": leave.id,
        "status": leave.status
    }

def get_leave_status(registration_number, limit=5):
    student_id = get_student_id_by_reg_no(registration_number)
    if not student_id:
        return {"error": "Student not found"}
        
    leaves = Leave.query.filter_by(student_id=student_id).order_by(Leave.id.desc()).limit(limit).all()
    
    if not leaves:
        return {"message": "You have no leave applications."}
        
    history = []
    for l in leaves:
        history.append({
            "leave_id": l.id,
            "type": l.type,
            "from_date": l.from_date.strftime("%d %b %Y"),
            "to_date": l.to_date.strftime("%d %b %Y"),
            "reason": l.reason,
            "status": l.status
        })
        
    return {
        "total_records": len(history),
        "leaves": history
    }
