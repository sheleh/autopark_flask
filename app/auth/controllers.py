import pdb
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jwt_identity
from flask_restful import Resource, abort
from flask import request, Response
from app.accounts.models import User
from .models import RevokedTokenModel
from app.schemas import user_login_form_schema


class UserLogin(Resource):
    """User login API"""
    def post(self):
        data = request.get_json()
        errors = user_login_form_schema.validate(data)
        if errors:
            abort(Response(f'Incorrect data {errors}', 400))
        email = data.get('email')
        current_user = User.find_by_email(email)
        # TODO: need to change this condition
        if not current_user:
            return {'message': f'User {email} does not exist'}
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
            return {'message': "wrong Credentials"}, 403


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except Exception as e:
            abort(Response(f'Something went wrong! {e}', 400))


class UserLogoutRefresh(Resource):
    """User Logout Refresh API"""

    @jwt_required
    def post(self):
        jti = get_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            pdb.set_trace()
            return {'message': 'Refresh token has been revoked'}
        except Exception as e:
            abort(Response(f'Something went wrong! {e}', 400))


class TokenRefresh(Resource):
    """Token Refresh API"""

    @jwt_required
    def post(self):
        # Generating new access token
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}
