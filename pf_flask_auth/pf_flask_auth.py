from pf_flask_auth.cli.pf_flask_auth_cli import pf_flask_auth_cli
from pf_flask_auth.common.pffa_auth_config import PFFAuthConfig
from pf_flask_auth.controller.operator_api_controller import operator_api_controller
from pf_flask_auth.controller.operator_form_controller import operator_form_controller
from pf_flask_auth.service.auth_interceptor_service import AuthInterceptorService


class PFFlaskAuth:
    auth_interceptor_service: AuthInterceptorService = AuthInterceptorService()

    def init_app(self, app):
        if not app:
            return
        if PFFAuthConfig.enableAPIEndPoints:
            app.register_blueprint(operator_api_controller)
        if PFFAuthConfig.enableFormEndPoints:
            app.register_blueprint(operator_form_controller)

        app.cli.add_command(pf_flask_auth_cli)
        app.before_request_funcs.setdefault(None, []).append(self.auth_interceptor_service.intercept)


pf_flask_auth = PFFlaskAuth()
