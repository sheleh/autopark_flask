from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify

from app.auth import models
from app.models import User


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            current_user_id = claims.get('id')
            user = User.query.get_or_404(current_user_id)
            if user.is_staff():
                return jsonify(msg='Administrator permission required'), 403
            else:
                return fn(*args, **kwargs), current_user_id
        return decorator
    return wrapper


def get_current_user():
    claims = get_jwt()
    current_user_id = claims.get('id')
    user = User.query.get_or_404(current_user_id)
    return user


# Checking that token is in blacklist or not
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)
