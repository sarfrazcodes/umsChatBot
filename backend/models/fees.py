from extensions import db

class Fee(db.Model):
    __tablename__ = 'fees'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    category = db.Column(db.String(50), nullable=False) # SEMESTER_FEE, RESIDENTIAL_FEE, EXAMINATION_FEE
    total_amount = db.Column(db.Float, nullable=False)
    paid_amount = db.Column(db.Float, nullable=False, default=0.0)
    due_date = db.Column(db.Date, nullable=False)
