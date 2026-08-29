from models import Fee, Student
from extensions import db

def get_student_id_by_reg_no(registration_number):
    student = Student.query.filter_by(registration_number=registration_number).first()
    return student.student_id if student else None

def get_fee_summary(registration_number, category=None):
    student_id = get_student_id_by_reg_no(registration_number)
    if not student_id:
        return {"error": "Student not found"}
        
    query = Fee.query.filter_by(student_id=student_id)
    if category:
        query = query.filter(Fee.category.ilike(f"%{category}%"))
        
    fees = query.all()
    if not fees:
        return {"message": "No fee records found."}
        
    total_amount = sum(f.total_amount for f in fees)
    total_paid = sum(f.paid_amount for f in fees)
    total_due = total_amount - total_paid
    
    breakdown = []
    for f in fees:
        due = f.total_amount - f.paid_amount
        breakdown.append({
            "category": f.category,
            "total_amount": f.total_amount,
            "paid_amount": f.paid_amount,
            "due_amount": due,
            "due_date": f.due_date.strftime("%d %b %Y") if f.due_date else None,
            "status": "Cleared" if due <= 0 else "Pending"
        })
        
    return {
        "total_amount": total_amount,
        "total_paid": total_paid,
        "total_due": total_due,
        "overall_status": "Cleared" if total_due <= 0 else "Pending",
        "breakdown": breakdown
    }

def get_fee_deadlines(registration_number):
    student_id = get_student_id_by_reg_no(registration_number)
    if not student_id:
        return {"error": "Student not found"}
        
    # Get all fees where due_amount > 0, ordered by due_date
    fees = Fee.query.filter_by(student_id=student_id).all()
    
    deadlines = []
    for f in fees:
        due = f.total_amount - f.paid_amount
        if due > 0 and f.due_date:
            deadlines.append({
                "category": f.category,
                "due_amount": due,
                "due_date": f.due_date.strftime("%d %b %Y"),
                "raw_date": f.due_date # for sorting
            })
            
    # Sort by closest deadline
    deadlines.sort(key=lambda x: x["raw_date"])
    
    # Remove raw_date before returning
    for d in deadlines:
        del d["raw_date"]
        
    if not deadlines:
        return {"message": "No pending fee deadlines."}
        
    return {
        "pending_deadlines": len(deadlines),
        "deadlines": deadlines
    }
