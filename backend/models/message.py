from extensions import db

class Message(db.Model):
    __tablename__ = 'messages'
    message_id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(255), nullable=True) # comma separated
    department = db.Column(db.String(100), nullable=True)
    priority = db.Column(db.String(20), nullable=False, default='Normal')
    published_at = db.Column(db.DateTime, nullable=False)
