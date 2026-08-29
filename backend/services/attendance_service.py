from models import Attendance, Student, Subject
from extensions import db

def get_student_id_by_reg_no(registration_number):
    student = Student.query.filter_by(registration_number=registration_number).first()
    return student.student_id if student else None

def get_overall_attendance(registration_number):
    student_id = get_student_id_by_reg_no(registration_number)
    if not student_id:
        return {"error": "Student not found"}
        
    records = Attendance.query.filter_by(student_id=student_id).all()
    if not records:
        return {"message": "No attendance records found.", "percentage": 0}
        
    total_attended = sum(r.attended_classes for r in records)
    total_conducted = sum(r.total_classes for r in records)
    
    if total_conducted == 0:
        return {"message": "No classes conducted yet.", "percentage": 0}
        
    percentage = (total_attended / total_conducted) * 100
    
    details = []
    for r in records:
        subject = Subject.query.filter_by(subject_code=r.subject_code).first()
        sub_pct = (r.attended_classes / r.total_classes * 100) if r.total_classes > 0 else 0
        details.append({
            "subject": subject.name if subject else r.subject_code,
            "code": r.subject_code,
            "attended": r.attended_classes,
            "total": r.total_classes,
            "percentage": round(sub_pct, 2)
        })
        
    return {
        "overall_percentage": round(percentage, 2),
        "total_attended": total_attended,
        "total_conducted": total_conducted,
        "details": details
    }

def run_absence_projection(registration_number, absent_days):
    # Assuming 1 day = 4 classes (1 for each subject for simplicity)
    student_id = get_student_id_by_reg_no(registration_number)
    if not student_id:
        return {"error": "Student not found"}
        
    records = Attendance.query.filter_by(student_id=student_id).all()
    
    total_attended = sum(r.attended_classes for r in records)
    total_conducted = sum(r.total_classes for r in records)
    
    current_percentage = (total_attended / total_conducted) * 100 if total_conducted > 0 else 0
    
    # Project absence
    new_total_conducted = total_conducted + (absent_days * 4) # rough estimate of classes missed
    new_percentage = (total_attended / new_total_conducted) * 100 if new_total_conducted > 0 else 0
    
    drop = current_percentage - new_percentage
    
    return {
        "current_percentage": round(current_percentage, 2),
        "projected_percentage": round(new_percentage, 2),
        "percentage_drop": round(drop, 2),
        "warning": new_percentage < 75.0
    }
