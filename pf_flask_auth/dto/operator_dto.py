from marshmallow import fields
from pf_flask_auth.common.pffa_auth_config import PFFAuthConfig
from pf_flask_rest.api.pf_app_api_def import APIBaseDef
from pf_flask_rest.form.pf_app_form_def import FormBaseDef, FormAppDef


class LoginDTO(FormBaseDef):
    identifier = fields.String(required=True, error_messages={"required": "Please enter identifier."})
    password = fields.String(required=True, error_messages={"required": "Please enter password."})


class LoginFormDTO(LoginDTO):
    rememberMe = fields.Boolean(default=False)


class OperatorDTO(FormAppDef, PFFAuthConfig.operatorDTOExtend):
    firstName = fields.String()
    lastName = fields.String()
    name = fields.String()
    email = fields.String()
    username = fields.String()


class LoginTokenDTO(APIBaseDef):
    accessToken = fields.String()
    refreshToken = fields.String()


class LoginResponseDTO(APIBaseDef):
    loginToken = fields.Nested(LoginTokenDTO)
    operator = fields.Nested(OperatorDTO)


class RefreshTokenDto(APIBaseDef):
    refreshToken = fields.String()


class RefreshTokenResponseDto(APIBaseDef):
    loginToken = fields.Nested(LoginTokenDTO)


class CreateCLIOperatorDTO(FormBaseDef):
    email = fields.Email(required=True, error_messages={"required": "Please enter email."})
    password = fields.String(required=True, error_messages={"required": "Please enter password."})
