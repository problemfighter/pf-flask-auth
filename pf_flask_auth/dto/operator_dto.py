from marshmallow import fields, validates_schema, ValidationError
from pf_flask_auth.common.pffa_auth_config import PFFAuthConfig
from pf_flask_rest.api.pf_app_api_def import APIBaseDef
from pf_flask_rest.form.pf_app_form_def import FormBaseDef, FormAppDef


class LoginDTO(FormBaseDef):
    identifier = fields.String(required=True, error_messages={"required": "Please enter identifier."})
    password = fields.String(required=True, error_messages={"required": "Please enter password."})


class LoginFormDTO(LoginDTO):
    rememberMe = fields.Boolean(default=False)


class LoginTokenDTO(APIBaseDef):
    accessToken = fields.String()
    refreshToken = fields.String()


class LoginResponseDTO(APIBaseDef):
    loginToken = fields.Nested(LoginTokenDTO)
    operator = fields.Nested(PFFAuthConfig.customOperatorDTO)


class RefreshTokenDTO(APIBaseDef):
    refreshToken = fields.String()


class RefreshTokenResponseDTO(APIBaseDef):
    loginToken = fields.Nested(LoginTokenDTO)


class CreateCLIOperatorDTO(FormBaseDef):
    email = fields.Email(required=True, error_messages={"required": "Please enter email."})
    password = fields.String(required=True, error_messages={"required": "Please enter password."})


class ResetPasswordDTO(FormBaseDef):
    newPassword = fields.String(required=True, error_messages={"required": "Please enter new password."})
    confirmPassword = fields.String(required=True, error_messages={"required": "Please enter confirm password."})
    token = fields.String(required=True, error_messages={"required": "Please enter token."})

    @validates_schema
    def validate_schema(self, data, **kwargs):
        if data["newPassword"] != data["confirmPassword"]:
            raise ValidationError("New password & confirm password not matched!", "confirmPassword")


class ForgotPasswordDTO(FormBaseDef):
    email = fields.String(required=True, error_messages={"required": "Please enter email."})
