from models import Timetable, Student, Subject, Faculty, FacultyLeave
from extensions import db
from datetime import datetime
import calendar

def get_student_id_by_reg_no(registration_number):
    student = Student.query.filter_by(registration_number=registration_number).first()
    return student.student_id if student else None

def get_todays_timetable(registration_number, specific_day=None):
    student_id = get_student_id_by_reg_no(registration_number)
    if not student_id:
        return {"error": "Student not found"}
        
    if not specific_day:
        # Get current day string (e.g. "Monday")
        today_date = datetime.today()
        specific_day = calendar.day_name[today_date.weekday()]
        
    classes = Timetable.query.filter_by(student_id=student_id, day=specific_day).order_by(Timetable.start_time).all()
    
    if not classes:
        return {"day": specific_day, "message": "You have no classes scheduled for this day.", "classes": []}
        
    schedule = []
    for c in classes:
        subject = Subject.query.filter_by(subject_code=c.subject_code).first()
        faculty = Faculty.query.filter_by(faculty_id=c.faculty_id).first()
        
        # Check if faculty is on leave today
        # In a real app we'd match the exact date. Here we'll do a simple mock check
        on_leave = False
        
        schedule.append({
            "subject": subject.name if subject else c.subject_code,
            "faculty": faculty.name if faculty else "Unknown",
            "room": c.room,
            "start_time": c.start_time.strftime("%H:%M"),
            "end_time": c.end_time.strftime("%H:%M"),
            "faculty_on_leave": on_leave
        })
        
    return {
        "day": specific_day,
        "total_classes": len(classes),
        "classes": schedule
    }
    
def get_next_class(registration_number):
    # For a real implementation, you check current time and find the next immediate class today
    # For this hackathon, we'll just reuse today's timetable and grab the first one as a mock
    res = get_todays_timetable(registration_number)
    if "error" in res:
        return res
        
    if not res.get("classes"):
        return {"message": "No more classes today."}
        
    return {"next_class": res["classes"][0]}
