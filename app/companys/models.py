from app import db
from app.accounts.models import User
from app.offices.models import Office


class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    address = db.Column(db.String(150))
    members = db.relationship('User', foreign_keys=[User.company_id], back_populates='company')
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    offices = db.relationship('Office', back_populates='company')
    vehicles = db.relationship('Vehicle',  back_populates='company')

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def check_office_exists(cls, office_id):
        return cls.query.join(cls.offices).filter(Office.id == office_id).first()

    def __init__(self, name, address, owner_id):
        self.name = name
        self.address = address
        self.owner_id = owner_id

    def __repr__(self):
        return self.name
