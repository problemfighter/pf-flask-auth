import os

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
            api_controller = operator_api_controller
            api_controller.url_prefix = PFFAuthConfig.apiUrlPrefix
            app.register_blueprint(api_controller)
        if PFFAuthConfig.enableFormEndPoints:
            form_controller = operator_form_controller
            form_controller.url_prefix = PFFAuthConfig.formUrlPrefix
            app.register_blueprint(form_controller)

        app.cli.add_command(pf_flask_auth_cli)
        app.before_request_funcs.setdefault(None, []).append(self.auth_interceptor_service.intercept)
        self._init_default_path()
        AuthInterceptorService.init_auth_skip_url()

    def _init_default_path(self):
        root_path = os.path.dirname(os.path.abspath(__file__))

        if not PFFAuthConfig.emailTemplatePath:
            email_template_path = os.path.join(root_path, "email-template")
            PFFAuthConfig.emailTemplatePath = email_template_path


pf_flask_auth = PFFlaskAuth()
