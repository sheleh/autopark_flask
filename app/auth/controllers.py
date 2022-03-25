from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jwt_identity
from flask_restful import Resource, abort
from flask import Response
from app.database.models import User, RevokedTokenModel
from app.schemas import user_login_form_schema
from app.utils import validate_request_data


class UserLogin(Resource):
    """User login API"""
    def post(self):
        data = validate_request_data(user_login_form_schema)
        email = data.get('email')
        current_user = User.find_by_email(email)
        if not current_user:
            return {'message': f'User {email} does not exist'}, 401
        if User.verify_hash(data.get('password'), current_user.password):
            additional_claims = {"id": current_user.id}
            access_token = create_access_token(identity=email, additional_claims=additional_claims)
            refresh_token = create_refresh_token(identity=email)
            return {
                'message': f'Logged in as {email}',
                'access_token': access_token,
                'refresh': refresh_token,
            }
        else:
            return {'message': "Wrong Credentials"}, 403


class UserLogout(Resource):
    """User logout API by revoking refresh token"""
    @jwt_required(refresh=True)
    def post(self):
        jti = get_jwt()['jti']
        try:
            revoked_refresh_token = RevokedTokenModel(jti=jti)
            revoked_refresh_token.add()
            return {'message': 'Refresh token has been revoked, User has been logged out'}
        except Exception as e:
            abort(Response(f'Something went wrong! {e}', 400))


class TokenRefresh(Resource):
    """Token Refresh API"""
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        current_user_obj = User.find_by_email(current_user)
        additional_claims = {"id": current_user_obj.id}
        access_token = create_access_token(identity=current_user_obj.email, additional_claims=additional_claims)
        return {'access_token': access_token}
