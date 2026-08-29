from models import Student, StudentMarks, GradingRules, Subject
from extensions import db

def get_student_by_reg_no(registration_number):
    return Student.query.filter_by(registration_number=registration_number).first()

def get_profile(registration_number):
    student = get_student_by_reg_no(registration_number)
    if not student:
        return {"error": "Student not found"}
        
    return {
        "registration_number": student.registration_number,
        "name": student.name,
        "cgpa": student.cgpa,
        "tgpa": student.tgpa,
        "branch": student.branch,
        "semester": student.semester,
        "backlogs": student.backlogs,
        "graduation_year": student.graduation_year
    }

def calculate_target_marks(registration_number, subject_code, target_grade):
    student = get_student_by_reg_no(registration_number)
    if not student:
        return {"error": "Student not found"}
        
    marks = StudentMarks.query.filter_by(student_id=student.student_id, subject_code=subject_code).first()
    if not marks:
        # Create dummy marks if none exist for demonstration purposes
        marks = StudentMarks(student_id=student.student_id, subject_code=subject_code, ca1=15, ca2=20, mid_term=25, end_term=None)
        db.session.add(marks)
        db.session.commit()
        
    rule = GradingRules.query.filter_by(grade=target_grade.upper()).first()
    if not rule:
        available_grades = [r.grade for r in GradingRules.query.all()]
        return {"error": f"Invalid target grade. Valid grades are: {', '.join(available_grades)}"}
        
    # Assume scoring: CA1 (30), CA2 (30), Mid (40), End (100)
    # Total internal = (CA1 + CA2) / 60 * 30 + (Mid / 40) * 20 => simplified math for demo:
    # Let's say Total Internal is out of 50. End term is out of 50. Total = 100.
    
    ca1 = marks.ca1
    ca2 = marks.ca2
    mid_term = marks.mid_term
    end_term = marks.end_term
    
    ca1_val = ca1 if ca1 is not None else 0
    ca2_val = ca2 if ca2 is not None else 0
    mid_val = mid_term if mid_term is not None else 0
    end_val = end_term if end_term is not None else 0
    
    # Internal scaled out of 50. End scaled out of 50.
    internal_score = ((ca1_val + ca2_val) / 60.0 * 25.0) + (mid_val / 40.0 * 25.0)
    total_scaled = internal_score + (end_val / 100.0 * 50.0)
    
    required_total = rule.min_percentage
    subject = Subject.query.filter_by(subject_code=subject_code).first()
    subject_name = subject.name if subject else subject_code
    
    missing_components = []
    existing_marks = []
    
    if end_term is None: missing_components.append("End Term")
    else: existing_marks.append(f"End Term: {end_term}/100")
        
    if mid_term is None: missing_components.append("Mid Term")
    else: existing_marks.append(f"Mid Term: {mid_term}/40")
        
    if ca2 is None: missing_components.append("CA2")
    else: existing_marks.append(f"CA2: {ca2}/30")
        
    if ca1 is None: missing_components.append("CA1")
    else: existing_marks.append(f"CA1: {ca1}/30")
        
    marks_summary = ""
    if existing_marks:
        marks_summary = f"Your current marks are **{', '.join(existing_marks)}**. "
    else:
        marks_summary = "You haven't received any marks yet. "
    
    if not missing_components:
        if total_scaled >= required_total:
            msg = f"You have already completed all exams and secured {round(total_scaled, 2)}%, which is enough for an {target_grade.upper()} grade!"
        else:
            msg = f"You have completed all exams but scored {round(total_scaled, 2)}%, which is not enough for an {target_grade.upper()} grade."
        return {"subject": subject_name, "message": marks_summary + msg, "possible": total_scaled >= required_total}
        
    marks_needed_scaled = required_total - total_scaled
    
    if marks_needed_scaled <= 0:
        return {
            "subject": subject_name,
            "target_grade": target_grade.upper(),
            "message": marks_summary + f"You already have enough marks to secure an {target_grade.upper()} grade! Just don't fail the remaining components.",
            "possible": True
        }
        
    if missing_components == ["End Term"]:
        req_end = marks_needed_scaled * 2
        if req_end > 100:
            msg = f"Unfortunately, you need {round(req_end, 2)}/100 in End Term, which is impossible."
            possible = False
        else:
            msg = f"You need to score at least {round(req_end, 2)} out of 100 in your End Term exam to get an {target_grade.upper()} in {subject_name}."
            possible = True
    elif "CA2" in missing_components and "End Term" in missing_components:
        req_end = (marks_needed_scaled - 12.5) * 2 # Assuming 30/30 in CA2 -> 12.5 scaled
        if req_end <= 100 and req_end > 0:
            msg = f"If you score full marks (30/30) in your upcoming CA2, you will only need {round(req_end, 2)}/100 in your End Term to get an {target_grade.upper()}."
            possible = True
        elif req_end > 100:
            msg = f"Even with full marks in CA2, you would need {round(req_end, 2)}/100 in End Term, which is impossible."
            possible = False
        else:
            msg = f"With full marks in CA2, you easily secure the {target_grade.upper()} grade."
            possible = True
    else:
        msg = f"You need {round(marks_needed_scaled, 2)} more overall percentage points. Focus on maximizing your upcoming {', '.join(missing_components)}!"
        possible = True
        
    return {
        "subject": subject_name,
        "target_grade": target_grade.upper(),
        "internal_score": round(internal_score, 2),
        "message": marks_summary + msg,
        "possible": possible
    }

def get_all_course_info(registration_number):
    student = get_student_by_reg_no(registration_number)
    if not student:
        return {"error": "Student not found"}
        
    from models import Attendance
    records = Attendance.query.filter_by(student_id=student.student_id).all()
    
    courses = []
    for r in records:
        subj = Subject.query.filter_by(subject_code=r.subject_code).first()
        pct = (r.attended_classes / r.total_classes * 100) if r.total_classes > 0 else 0
        courses.append({
            "code": r.subject_code,
            "name": subj.name if subj else "Unknown",
            "credits": subj.credits if subj else 3,
            "attendance": round(pct, 2)
        })
        
    return {"courses": courses}
