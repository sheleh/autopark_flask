from .controllers import UserLogin, UserLogout, TokenRefresh


def auth_module_routes(api):
    api.add_resource(UserLogin, '/api/login')
    api.add_resource(UserLogout, '/api/logout')
    api.add_resource(TokenRefresh, '/api/token/refresh')
