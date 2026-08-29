from extensions import db

class LibraryBook(db.Model):
    __tablename__ = 'library_books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    keywords = db.Column(db.Text, nullable=True)
    building = db.Column(db.String(50), nullable=False)
    floor = db.Column(db.Integer, nullable=False)
    shelf = db.Column(db.String(20), nullable=False)
    total_copies = db.Column(db.Integer, nullable=False)
    available_copies = db.Column(db.Integer, nullable=False)
