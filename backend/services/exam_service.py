from models import Exam, Student, Subject
from extensions import db
from datetime import datetime

def get_student_id_by_reg_no(registration_number):
    student = Student.query.filter_by(registration_number=registration_number).first()
    return student.student_id if student else None

def get_upcoming_exams(registration_number, limit=None):
    student_id = get_student_id_by_reg_no(registration_number)
    if not student_id:
        return {"error": "Student not found"}
        
    # In a real app we'd filter by date >= today.
    # For mock data we just order by date ascending
    query = Exam.query.filter_by(student_id=student_id).order_by(Exam.date.asc(), Exam.time.asc())
    
    if limit:
        query = query.limit(limit)
        
    exams = query.all()
    
    if not exams:
        return {"message": "No upcoming exams found.", "exams": []}
        
    exam_list = []
    for exam in exams:
        subject = Subject.query.filter_by(subject_code=exam.subject_code).first()
        exam_list.append({
            "subject_code": exam.subject_code,
            "subject_name": subject.name if subject else "Unknown",
            "date": exam.date.strftime("%d %b %Y"),
            "time": exam.time.strftime("%H:%M"),
            "venue": exam.venue,
            "syllabus": subject.syllabus if subject else "N/A"
        })
        
    return {
        "total_exams": len(exams),
        "exams": exam_list
    }

def get_exam_syllabus(subject_code):
    subject = Subject.query.filter_by(subject_code=subject_code).first()
    if not subject:
        return {"error": f"Subject code {subject_code} not found."}
        
    return {
        "subject_code": subject.subject_code,
        "subject_name": subject.name,
        "syllabus": subject.syllabus
    }
