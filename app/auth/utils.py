from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask_restful import abort
from app.database.models import User
from flask import Response


def admin_required():

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            current_user_id = claims.get('id')
            user = User.query.get_or_404(current_user_id)
            if user.is_staff():
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
