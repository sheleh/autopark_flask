from app import db


class Office(db.Model):
    """Office model"""
    __tablename__ = 'office'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    country = db.Column(db.String)
    city = db.Column(db.String)
    region = db.Column(db.String)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    company = db.relationship('Company', back_populates='offices')
    worker = db.relationship("User", back_populates="office")
    vehicles = db.relationship('Vehicle', back_populates='office')

    @classmethod
    def check_on_unique_name(cls, name, company_id):
        return cls.query.filter_by(name=name, company_id=company_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def __init__(self, name, address, country, city, region, company_id):
        self.name = name
        self.address = address
        self.country = country
        self.city = city
        self.region = region
        self.company_id = company_id

    def __repr__(self):
        return self.name
