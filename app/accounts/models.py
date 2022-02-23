from app import db
from passlib.hash import pbkdf2_sha256 as sha256

drivers_association_table = db.Table('drivers_association', db.metadata,
                                     db.Column('user_id', db.ForeignKey('user.id'), primary_key=True),
                                     db.Column('vehicle_id', db.ForeignKey('vehicle.id'), primary_key=True)
                                     )


class User(db.Model):
    """User model class"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(70))
    last_name = db.Column(db.String(70))
    is_stafff = db.Column(db.Boolean(), default=True)
    chief_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)
    company = db.relationship('Company', back_populates="members", foreign_keys=[company_id])
    office_id = db.Column(db.Integer, db.ForeignKey('office.id'), nullable=True)
    office = db.relationship('Office', back_populates="worker", foreign_keys=[office_id])
    vehicle = db.relationship('Vehicle', secondary=drivers_association_table, back_populates='driver')

    def __init__(self, email, password, first_name, last_name, chief_id, company_id, office_id, is_stafff):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.chief_id = chief_id
        self.company_id = company_id
        self.office_id = office_id
        self.is_stafff = is_stafff

    """Save user details to DataBase"""
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    """Delete user from DataBase"""
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def is_staff(self):
        return self.is_stafff

    """generate hash from password using sha256 encryption"""
    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    """verify hash and password"""
    @staticmethod
    def verify_hash(password, hash_):
        return sha256.verify(password, hash_)

    def __repr__(self):
        return str(self.email)
