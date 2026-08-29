from extensions import db

class PlacementDrive(db.Model):
    __tablename__ = 'placement_drives'
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    min_cgpa = db.Column(db.Float, nullable=False)
    min_tgpa = db.Column(db.Float, nullable=False)
    allowed_branches = db.Column(db.String(255), nullable=False) # comma separated
    deadline = db.Column(db.Date, nullable=False)

class PlacementRegistration(db.Model):
    __tablename__ = 'placement_registrations'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drives.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Registered')
