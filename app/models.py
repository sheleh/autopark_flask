from app import db
from passlib.hash import pbkdf2_sha256 as sha256


class User(db.Model):
    """User model class"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(70))
    last_name = db.Column(db.String(70))
    is_stafff = db.Column(db.Boolean(), default=True)
    chief_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)
    company = db.relationship('Company', back_populates="members", foreign_keys=[company_id])

    def __init__(self, email, password, first_name, last_name, chief_id, company_id):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.chief_id = chief_id
        self.company_id = company_id
        # self.company = company

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


class Company(db.Model):
    """ Company model"""
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    address = db.Column(db.String(150))
    members = db.relationship('User', foreign_keys=[User.company_id], back_populates='company')
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    offices = db.relationship('Office', back_populates='company')

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def __init__(self, name, address, owner_id):
        self.name = name
        self.address = address
        self.owner_id = owner_id

    def __repr__(self):
        return self.name


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

    def __init__(self, name, address, country, city, region):
        self.name = name
        self.address = address
        self.country = country
        self.city = city
        self.region = region



class RevokedTokenModel(db.Model):
    """Revoked Token Model Class"""
    __tablename__ = 'revoked_tokens'
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
