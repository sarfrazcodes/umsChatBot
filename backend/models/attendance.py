from extensions import db

class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    subject_code = db.Column(db.String(20), db.ForeignKey('subjects.subject_code'), nullable=False)
    attended_classes = db.Column(db.Integer, nullable=False, default=0)
    total_classes = db.Column(db.Integer, nullable=False, default=0)
