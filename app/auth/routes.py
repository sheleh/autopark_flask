from .controllers import UserLogin, UserLogoutAccess, UserLogoutRefresh, TokenRefresh


def auth_module_routes(api):
    api.add_resource(UserLogin, '/login')
    api.add_resource(UserLogoutAccess, '/logout/access')
    api.add_resource(UserLogoutRefresh, '/logout/refresh')
    api.add_resource(TokenRefresh, '/token/refresh')
