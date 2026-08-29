from extensions import db

class Student(db.Model):
    __tablename__ = 'students'
    student_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    registration_number = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    cgpa = db.Column(db.Float, nullable=False, default=0.0)
    tgpa = db.Column(db.Float, nullable=False, default=0.0)
    branch = db.Column(db.String(50), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    backlogs = db.Column(db.Integer, nullable=False, default=0)
    graduation_year = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', back_populates='student')
