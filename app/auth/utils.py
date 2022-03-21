from functools import wraps

import jwt
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask_restful import abort
from app.database.models import User, RevokedTokenModel
from flask import Response


def admin_required():

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            current_user_id = claims.get('id')
            user = User.query.get_or_404(current_user_id)
            if user.is_stafff:
                abort(Response('Administrator permission required', 403))
            else:
                return fn(*args, **kwargs)
        return decorator
    return wrapper


def get_current_user():
    claims = get_jwt()
    current_user_id = claims.get('id')
    user = User.query.get_or_404(current_user_id)
    return user


def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)

# def check_token_in_blacklist():
#     claims = get_jwt()
#     if RevokedTokenModel.is_jti_blacklisted(claims):
#         abort(Response('This token is revoked', 403))

# Checking that token is in blacklist or not
# def check_if_token_in_blacklist(decrypted_token):
#     jti = decrypted_token['jti']
#     return RevokedTokenModel.is_jti_blacklisted(jti)
