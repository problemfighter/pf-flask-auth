from pf_flask_auth.common.pffa_auth_config import PFFAuthConfig
from pf_flask_auth.controller.operator_api_controller import operator_api_controller
from pf_flask_auth.controller.operator_form_controller import operator_form_controller


class PFFlaskAuth:

    def init_app(self, app):
        if PFFAuthConfig.enableAPIEndPoints:
            app.register_blueprint(operator_api_controller)
        if PFFAuthConfig.enableFormEndPoints:
            app.register_blueprint(operator_form_controller)


pf_flask_auth = PFFlaskAuth()
