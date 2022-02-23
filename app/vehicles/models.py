from app import db
from app.accounts.models import drivers_association_table


class Vehicle(db.Model):
    """Office model"""
    __tablename__ = 'vehicle'
    id = db.Column(db.Integer, primary_key=True)
    license_plate = db.Column(db.String, nullable=False)
    name = db.Column(db.String)
    model = db.Column(db.String)
    year_of_manufacture = db.Column(db.Integer)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    company = db.relationship('Company', back_populates='vehicles')
    office_id = db.Column(db.Integer, db.ForeignKey('office.id'), nullable=True)
    office = db.relationship('Office', back_populates='vehicles')
    driver = db.relationship('User', secondary=drivers_association_table, back_populates='vehicle')

    @classmethod
    def check_on_unique_license_plate(cls, license_plate):
        return cls.query.filter_by(license_plate=license_plate).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def __init__(self, license_plate, name, model, year_of_manufacture, company_id, office_id):
        self.license_plate = license_plate
        self.name = name
        self.model = model
        self.year_of_manufacture = year_of_manufacture
        self.company_id = company_id
        self.office_id = office_id

    def __repr__(self):
        return self.name
