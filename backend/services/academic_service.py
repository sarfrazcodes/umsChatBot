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
    
    ca1 = marks.ca1 or 0
    ca2 = marks.ca2 or 0
    mid_term = marks.mid_term or 0
    
    # Internal scaled out of 50 (Assuming CA1 is 30, CA2 is 30, Mid is 40 raw)
    internal_score = ((ca1 + ca2) / 60.0 * 25.0) + (mid_term / 40.0 * 25.0)
    
    required_total = rule.min_percentage
    required_end_term = required_total - internal_score
    
    # Scale end term back to out of 100 (if it contributes 50% to final grade)
    required_end_term_raw = required_end_term * 2
    
    subject = Subject.query.filter_by(subject_code=subject_code).first()
    subject_name = subject.name if subject else subject_code
    
    if required_end_term_raw > 100:
        return {
            "subject": subject_name,
            "target_grade": target_grade.upper(),
            "internal_score": round(internal_score, 2),
            "message": f"Unfortunately, even if you score 100/100 in the End Term, you cannot achieve an {target_grade.upper()} grade.",
            "possible": False
        }
    elif required_end_term_raw <= 0:
        return {
            "subject": subject_name,
            "target_grade": target_grade.upper(),
            "internal_score": round(internal_score, 2),
            "message": f"You already have enough internal marks to secure an {target_grade.upper()} grade! Just don't fail.",
            "possible": True,
            "required_end_term": 0
        }
    else:
        return {
            "subject": subject_name,
            "target_grade": target_grade.upper(),
            "internal_score": round(internal_score, 2),
            "required_total": required_total,
            "required_end_term_out_of_100": round(required_end_term_raw, 2),
            "message": f"You need to score at least {round(required_end_term_raw, 2)} out of 100 in your End Term exam to get an {target_grade.upper()} in {subject_name}.",
            "possible": True
        }
