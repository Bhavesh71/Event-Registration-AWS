from app import db

class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    venue = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    num_people = db.Column(db.Integer, nullable=False)
    poster = db.Column(db.String(200), nullable=True)
    
    club = db.relationship('Club', backref=db.backref('events', lazy=True))
