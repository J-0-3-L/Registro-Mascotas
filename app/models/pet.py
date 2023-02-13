from app import db
from datetime import datetime

class Pet(db.Model):
    __tablename__ = 'pets'
    id = db.Column(db.Integer, primary_key=True)
    name_pet = db.Column(db.String(100), index=True, unique=True, nullable=False)
    race = db.Column(db.String(120), index=True, unique=True, nullable=False)
    birthdate = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_dict(self):
        pet = {
            'pet_id': self.id,
            'name_pet': self.name_pet,
            'race': self.race,
            'birthdate':self.birthdate,
            'owner_id': self.user_id
        }
        return pet