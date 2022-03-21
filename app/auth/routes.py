from .controllers import UserLogin, UserLogoutAccess, UserLogoutRefresh, TokenRefresh


def auth_module_routes(api):
    api.add_resource(UserLogin, '/api/login')
    api.add_resource(UserLogoutAccess, '/api/logout')
    api.add_resource(UserLogoutRefresh, '/api/logout/refresh')
    api.add_resource(TokenRefresh, '/api/token/refresh')
