from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy.orm import relationship, backref
from flask_sqlalchemy import SQLAlchemy
from flask_restful import abort
from flask import Response

db = SQLAlchemy()

drivers_association_table = db.Table(
    'drivers_association', db.metadata,
    db.Column('user_id', db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('vehicle_id', db.ForeignKey('vehicle.id', ondelete='CASCADE'), primary_key=True))


class User(db.Model):
    """User model class"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    chief_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='SET NULL'), nullable=True)
    company = db.relationship('Company', back_populates="members", foreign_keys=[company_id], passive_deletes=True)
    office_id = db.Column(db.Integer, db.ForeignKey('office.id', ondelete='SET NULL'), nullable=True)
    office = db.relationship(
        'Office', back_populates="worker", foreign_keys=[office_id], post_update=True, passive_deletes=True
    )
    vehicle = db.relationship(
        'Vehicle', secondary=drivers_association_table, back_populates='driver', post_update=True
    )

    def __init__(self, email, password, first_name, last_name, chief_id, company_id, office_id):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.chief_id = chief_id
        self.company_id = company_id
        self.office_id = office_id

    """Save user details to DataBase"""

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            abort(Response(f'Something went wrong! {e}', 400))

    """Delete user from DataBase"""
    def delete_from_db(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            abort(Response(f'Something went wrong! {e}', 400))

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def is_staff(self):
        return bool(self.chief_id)

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


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    address = db.Column(db.String)
    members = db.relationship(
        'User', foreign_keys=[User.company_id], back_populates='company', post_update=True, passive_deletes=True
    )
    owner_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', use_alter=True), nullable=True, unique=True
    )
    owner = db.relationship(
        'User', foreign_keys=[owner_id], backref=backref('company_owner', uselist=False), passive_deletes=True
    )
    offices = db.relationship('Office', back_populates='company', post_update=True)
    vehicles = db.relationship('Vehicle',  back_populates='company', post_update=True)

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            abort(Response(f'Something went wrong! {e}', 400))

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def check_by_owner(cls, owner_id):
        return cls.query.filter_by(owner_id=owner_id).first()

    @classmethod
    def check_office_exists(cls, office_id):
        return cls.query.join(cls.offices).filter(Office.id == office_id).first()

    def __init__(self, name, address, owner_id):
        self.name = name
        self.address = address
        self.owner_id = owner_id

    def __repr__(self):
        return self.name


class RevokedTokenModel(db.Model):
    """Revoked Token Model Class"""
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    """Save token to DB"""
    def add(self):
        db.session.add(self)
        db.session.commit()

    """Checking that token is blacklisted"""
    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)


class Office(db.Model):
    """Office model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    country = db.Column(db.String)
    city = db.Column(db.String)
    region = db.Column(db.String)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete="CASCADE"), nullable=True)
    company = relationship(
        'Company', foreign_keys=[company_id], back_populates='offices', cascade="all, delete", post_update=True
    )
    worker = relationship("User", back_populates="office",  post_update=True, passive_deletes=True)
    vehicles = relationship('Vehicle', back_populates='office')

    @classmethod
    def check_on_unique_name(cls, name, company_id):
        return cls.query.filter_by(name=name, company_id=company_id).first()

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            abort(Response(f'Something went wrong! {e}', 400))

    def delete_from_db(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            abort(Response(f'Something went wrong! {e}', 400))

    def __init__(self, name, address, country, city, region, company_id):
        self.name = name
        self.address = address
        self.country = country
        self.city = city
        self.region = region
        self.company_id = company_id

    def __repr__(self):
        return self.name


class Vehicle(db.Model):
    """Office model"""
    id = db.Column(db.Integer, primary_key=True)
    license_plate = db.Column(db.String, nullable=False)
    name = db.Column(db.String)
    model = db.Column(db.String)
    year_of_manufacture = db.Column(db.Integer)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='SET NULL'), nullable=True)
    company = relationship('Company', back_populates='vehicles')
    office_id = db.Column(db.Integer, db.ForeignKey('office.id', ondelete='SET NULL'), nullable=True)
    office = relationship('Office', back_populates='vehicles')
    driver = relationship('User', secondary=drivers_association_table, back_populates='vehicle')

    @classmethod
    def check_on_unique_license_plate(cls, license_plate):
        return cls.query.filter_by(license_plate=license_plate).first()

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            abort(Response(f'Something went wrong! {e}', 400))

    def delete_from_db(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            abort(Response(f'Something went wrong! {e}', 400))

    def __init__(self, license_plate, name, model, year_of_manufacture, company_id, office_id):
        self.license_plate = license_plate
        self.name = name
        self.model = model
        self.year_of_manufacture = year_of_manufacture
        self.company_id = company_id
        self.office_id = office_id

    def __repr__(self):
        return self.name
