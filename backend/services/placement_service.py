from models import PlacementDrive, PlacementRegistration, Student
from extensions import db
from datetime import date

def get_student_id_by_reg_no(registration_number):
    student = Student.query.filter_by(registration_number=registration_number).first()
    return student

def get_eligible_drives(registration_number):
    student = get_student_id_by_reg_no(registration_number)
    if not student:
        return {"error": "Student not found"}
        
    today = date.today()
    # Fetch all active drives
    active_drives = PlacementDrive.query.filter(PlacementDrive.deadline >= today).all()
    
    eligible = []
    ineligible = []
    
    for d in active_drives:
        # Check eligibility
        is_eligible = True
        reason = ""
        
        if student.cgpa < d.min_cgpa:
            is_eligible = False
            reason = f"CGPA ({student.cgpa}) is below required ({d.min_cgpa})"
        elif student.tgpa < d.min_tgpa:
            is_eligible = False
            reason = f"TGPA ({student.tgpa}) is below required ({d.min_tgpa})"
        elif student.branch not in d.allowed_branches:
            is_eligible = False
            reason = f"Branch ({student.branch}) not allowed."
            
        # Check if already registered
        registered = PlacementRegistration.query.filter_by(student_id=student.student_id, drive_id=d.id).first()
        status = registered.status if registered else "Not Registered"
        
        drive_info = {
            "drive_id": d.id,
            "company": d.company,
            "role": d.role,
            "deadline": d.deadline.strftime("%d %b %Y"),
            "status": status
        }
        
        if is_eligible:
            eligible.append(drive_info)
        else:
            drive_info["reason"] = reason
            ineligible.append(drive_info)
            
    return {
        "eligible_drives": eligible,
        "ineligible_drives": ineligible
    }

def register_for_drive(registration_number, drive_id):
    student = get_student_id_by_reg_no(registration_number)
    if not student:
        return {"error": "Student not found"}
        
    drive = PlacementDrive.query.get(drive_id)
    if not drive:
        return {"error": "Placement drive not found"}
        
    # Verify eligibility again just in case
    if student.cgpa < drive.min_cgpa or student.branch not in drive.allowed_branches:
        return {"error": "You are not eligible for this drive."}
        
    # Check if already registered
    existing = PlacementRegistration.query.filter_by(student_id=student.student_id, drive_id=drive.id).first()
    if existing:
        return {"message": f"You are already registered for {drive.company}."}
        
    new_reg = PlacementRegistration(student_id=student.student_id, drive_id=drive.id, status="Registered")
    db.session.add(new_reg)
    db.session.commit()
    
    return {"message": f"Successfully registered for {drive.company} ({drive.role}). Best of luck!"}
