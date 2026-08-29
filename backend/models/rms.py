from extensions import db

class RMSCategory(db.Model):
    __tablename__ = 'rms_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('rms_categories.id'), nullable=True)

class RMSRequest(db.Model):
    __tablename__ = 'rms_requests'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('rms_categories.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Open')
