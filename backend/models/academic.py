from extensions import db

class Subject(db.Model):
    __tablename__ = 'subjects'
    subject_code = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    syllabus = db.Column(db.Text, nullable=True)
    course_outcomes = db.Column(db.Text, nullable=True)

class Faculty(db.Model):
    __tablename__ = 'faculty'
    faculty_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)

class FacultyLeave(db.Model):
    __tablename__ = 'faculty_leave'
    leave_id = db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.faculty_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)

class Timetable(db.Model):
    __tablename__ = 'timetable'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    subject_code = db.Column(db.String(20), db.ForeignKey('subjects.subject_code'), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.faculty_id'), nullable=False)
    day = db.Column(db.String(20), nullable=False) # e.g. Monday
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    room = db.Column(db.String(20), nullable=False)
    section = db.Column(db.String(10), nullable=False)

class GradingRules(db.Model):
    __tablename__ = 'grading_rules'
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(5), nullable=False, unique=True)
    min_percentage = db.Column(db.Float, nullable=False)

class StudentMarks(db.Model):
    __tablename__ = 'student_marks'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    subject_code = db.Column(db.String(20), db.ForeignKey('subjects.subject_code'), nullable=False)
    ca1 = db.Column(db.Float, nullable=True)
    ca2 = db.Column(db.Float, nullable=True)
    mid_term = db.Column(db.Float, nullable=True)
    end_term = db.Column(db.Float, nullable=True)
