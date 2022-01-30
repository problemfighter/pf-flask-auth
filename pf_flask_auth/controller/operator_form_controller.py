from flask import Blueprint, render_template, redirect

from pf_flask_auth.common.pffa_auth_message import PFFAuthMessage
from pf_flask_auth.dto.operator_dto import LoginFormDTO, ResetPasswordDTO, ForgotPasswordDTO
from pf_flask_auth.common.pffa_auth_config import PFFAuthConfig
from pf_flask_auth.service.operator_form_service import OperatorFormService

url_prefix = PFFAuthConfig.formUrlPrefix
operator_form_controller = Blueprint(
    "operator_form_controller",
    __name__,
    url_prefix=url_prefix,
    template_folder="templates",
    static_folder="static",
    static_url_path="static",
)

operator_form_service = OperatorFormService()


@operator_form_controller.route("/", methods=['POST', 'GET'])
@operator_form_controller.route(PFFAuthConfig.loginURL, methods=['POST', 'GET'])
def login():
    form = LoginFormDTO()
    if form.is_post_request() and form.is_valid_data():
        if operator_form_service.login(form):
            return redirect(PFFAuthConfig.successRedirect)
    data = {
        "identifier": PFFAuthConfig.loginIdentifier,
        "name": PFFAuthConfig.loginViewName,
    }
    return render_template("auth/login.html", data=data, form=form.definition)


@operator_form_controller.route(PFFAuthConfig.resetPasswordURL + "/<string:token>", methods=['POST', 'GET'])
def reset_password(token: str):
    if not operator_form_service.is_valid_rest_password_token(token):
        return render_template("auth/reset-password-response.html", message=PFFAuthMessage.INVALID_TOKEN_OR_EXPIRE, error=True)
    form = ResetPasswordDTO()
    if form.is_post_request() and form.is_valid_data():
        if operator_form_service.reset_password(form):
            return render_template("auth/reset-password-response.html", message=PFFAuthMessage.PASS_RESET_SUCCESS, error=False)
        else:
            return render_template("auth/reset-password-response.html", message=PFFAuthMessage.INVALID_TOKEN_OR_EXPIRE, error=True)
    data = {}
    return render_template("auth/reset-password.html", data=data, form=form.definition, token=token)


@operator_form_controller.route(PFFAuthConfig.forgotPasswordURL, methods=['POST', 'GET'])
def forgot_password():
    form = ForgotPasswordDTO()
    if form.is_post_request() and form.is_valid_data():
        if operator_form_service.forgot_password(form):
            return render_template("auth/forgot-password-response.html")
    data = {
        "identifier": PFFAuthConfig.loginIdentifier,
        "name": PFFAuthConfig.loginViewName,
    }
    return render_template("auth/forgot-password.html", data=data, form=form.definition)


@operator_form_controller.route(PFFAuthConfig.logoutURL, methods=['GET'])
def logout():
    operator_form_service.logout()
    return redirect(url_prefix)
