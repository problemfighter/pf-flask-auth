from flask import Blueprint
from pf_flask_auth.common.pffa_auth_config import PFFAuthConfig

url_prefix = PFFAuthConfig.form_url_prefix
operator_form_controller = Blueprint("operator_form_controller", __name__, url_prefix=url_prefix)


@operator_form_controller.route("/")
@operator_form_controller.route("/login", methods=['POST', 'GET'])
def login():
    return "Login"


@operator_form_controller.route("/change-password", methods=['POST', 'GET'])
def change_password():
    return "change-password"


@operator_form_controller.route("/reset-password", methods=['POST', 'GET'])
def reset_password():
    return "reset-password"


@operator_form_controller.route("/forgot-password", methods=['POST', 'GET'])
def forgot_password():
    return "forgot-password"
