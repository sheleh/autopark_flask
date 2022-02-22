from app import db


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
