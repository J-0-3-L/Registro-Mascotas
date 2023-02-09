from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True, nullable=False)
    dni = db.Column(db.String(120), index=True, unique=True, nullable=False)
    pets = db.relationship('Pet', backref='user', lazy='dynamic')