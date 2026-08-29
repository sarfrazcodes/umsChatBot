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

def run_subject_absence_projection(registration_number, subject_query, absent_classes=1):
    student_id = get_student_id_by_reg_no(registration_number)
    if not student_id:
        return {"error": "Student not found"}
        
    records = Attendance.query.filter_by(student_id=student_id).all()
    if not records:
        return {"error": "No attendance records found."}
        
    target_record = None
    target_subject_name = None
    for r in records:
        subject = Subject.query.filter_by(subject_code=r.subject_code).first()
        sub_name = subject.name.lower() if subject else ""
        sub_code = r.subject_code.lower()
        query_lower = subject_query.lower()
        if query_lower in sub_name or query_lower in sub_code:
            target_record = r
            target_subject_name = subject.name if subject else r.subject_code
            break
            
    if not target_record:
        return {"error": f"Could not find a subject matching '{subject_query}' in your attendance records."}
        
    cur_sub_attended = target_record.attended_classes
    cur_sub_total = target_record.total_classes
    cur_sub_pct = (cur_sub_attended / cur_sub_total) * 100 if cur_sub_total > 0 else 0
    
    proj_sub_total = cur_sub_total + absent_classes
    proj_sub_pct = (cur_sub_attended / proj_sub_total) * 100 if proj_sub_total > 0 else 0
    sub_drop = cur_sub_pct - proj_sub_pct
    
    total_attended = sum(r.attended_classes for r in records)
    total_conducted = sum(r.total_classes for r in records)
    cur_overall_pct = (total_attended / total_conducted) * 100 if total_conducted > 0 else 0
    
    proj_overall_total = total_conducted + absent_classes
    proj_overall_pct = (total_attended / proj_overall_total) * 100 if proj_overall_total > 0 else 0
    overall_drop = cur_overall_pct - proj_overall_pct
    
    return {
        "subject": target_subject_name,
        "current_subject_pct": round(cur_sub_pct, 2),
        "projected_subject_pct": round(proj_sub_pct, 2),
        "subject_drop": round(sub_drop, 2),
        "current_overall_pct": round(cur_overall_pct, 2),
        "projected_overall_pct": round(proj_overall_pct, 2),
        "overall_drop": round(overall_drop, 2),
        "warning": proj_sub_pct < 75.0 or proj_overall_pct < 75.0
    }
