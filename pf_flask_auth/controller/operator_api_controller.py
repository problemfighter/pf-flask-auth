from flask import Blueprint
from pf_flask_auth.dto.operator_dto import LoginDTO, LoginResponseDTO, ForgotPasswordDTO, ResetPasswordDTO, \
    RefreshTokenDTO, RefreshTokenResponseDTO
from pf_flask_auth.common.pffa_auth_config import PFFAuthConfig
from pf_flask_swagger.swagger.pf_swagger_decorator import rest_request

url_prefix = PFFAuthConfig.apiUrlPrefix
operator_api_controller = Blueprint("operator_api_controller", __name__, url_prefix=url_prefix)


@operator_api_controller.route(PFFAuthConfig.loginURL, methods=['POST'])
@rest_request(request_obj=LoginDTO, response_obj=LoginResponseDTO)
def login():
    pass


@operator_api_controller.route(PFFAuthConfig.resetPasswordURL, methods=['POST'])
@rest_request(request_obj=ResetPasswordDTO, pf_message_response=True)
def reset_password():
    pass


@operator_api_controller.route(PFFAuthConfig.forgotPasswordURL, methods=['POST'])
@rest_request(request_obj=ForgotPasswordDTO, pf_message_response=True)
def forgot_password():
    pass


@operator_api_controller.route(PFFAuthConfig.logoutURL, methods=['GET'])
@rest_request(pf_message_response=True)
def logout():
    pass


@operator_api_controller.route(PFFAuthConfig.renewTokenURL, methods=['POST'])
@rest_request(request_obj=RefreshTokenDTO, response_obj=RefreshTokenResponseDTO)
def renew_token():
    pass
