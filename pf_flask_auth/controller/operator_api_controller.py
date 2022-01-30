from flask import Blueprint
from pf_flask_auth.common.pffa_auth_config import PFFAuthConfig

url_prefix = PFFAuthConfig.apiUrlPrefix
operator_api_controller = Blueprint("operator_api_controller", __name__, url_prefix=url_prefix)


@operator_api_controller.route(PFFAuthConfig.loginURL, methods=['POST'])
def login():
    pass


@operator_api_controller.route(PFFAuthConfig.resetPasswordURL, methods=['POST'])
def reset_password():
    pass


@operator_api_controller.route(PFFAuthConfig.forgotPasswordURL, methods=['POST'])
def forgot_password():
    pass


@operator_api_controller.route(PFFAuthConfig.logoutURL, methods=['GET'])
def logout():
    pass
