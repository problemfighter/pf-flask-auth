from sqlalchemy import and_
from pf_flask_auth.common.pffa_auth_config import PFFAuthConfig
from pf_flask_auth.common.pffa_auth_const import PFFAuthConst
from pf_flask_auth.common.pffa_auth_interceptor_abc import AuthInterceptOnVerifyABC, AuthCustomLoginABC
from pf_flask_auth.common.pffa_auth_message import PFFAuthMessage
from pf_flask_auth.common.pffa_jwt_helper import JWTHelper
from pf_flask_auth.model.pffa_default_model import DefaultModel
from pf_flask_auth.service.operator_email_service import OperatorEmailService
from pf_flask_rest_com.common.pffr_exception import pffrc_exception
from pf_py_common.py_common import PyCommon


class OperatorService:
    jwt_helper = JWTHelper()
    operator_email_service = OperatorEmailService()

    def get_operator_by_email(self, email):
        return DefaultModel.OperatorModel.query.filter(DefaultModel.OperatorModel.email == email, DefaultModel.OperatorModel.isDeleted == False).first()

    def get_operator_by_token(self, token):
        return DefaultModel.OperatorModel.query.filter(DefaultModel.OperatorModel.token == token, DefaultModel.OperatorModel.isDeleted == False).first()

    def get_operator_by_username(self, username):
        return DefaultModel.OperatorModel.query.filter(and_(DefaultModel.OperatorModel.username == username, DefaultModel.OperatorModel.isDeleted == False)).first()

    def get_operator_by_id(self, model_id):
        return DefaultModel.OperatorModel.query.filter(and_(DefaultModel.OperatorModel.id == model_id, DefaultModel.OperatorModel.isDeleted == False)).first()

    def get_operator_by_identifier(self, identifier):
        if PFFAuthConfig.loginIdentifier == PFFAuthConst.USERNAME:
            return self.get_operator_by_username(identifier)
        else:
            return self.get_operator_by_email(identifier)

    def create_operator_by_email(self, email, password):
        operator = self.get_operator_by_email(email)
        if operator:
            raise pffrc_exception.error_message_exception(PFFAuthMessage.OPERATOR_EXIST)

        operator = DefaultModel.OperatorModel()
        operator.email = email
        operator.password = password
        operator.save()
        if operator.id:
            return operator
        raise pffrc_exception.error_message_exception(PFFAuthMessage.OPERATOR_CREATE_ERROR)

    def reset_password_by_email(self, email, password):
        operator = self.get_operator_by_email(email)
        if not operator:
            raise pffrc_exception.error_message_exception(PFFAuthMessage.OPERATOR_NOT_EXIST)
        operator.password = password
        operator.save()
        if operator.id:
            return operator
        raise pffrc_exception.error_message_exception(PFFAuthMessage.OPERATOR_PASS_RESET_ERROR)

    def is_operator_email_exist(self, email):
        if self.get_operator_by_email(email):
            return True
        return False

    def is_other_operator_email_exist(self, email, model_id):
        operator = DefaultModel.OperatorModel.query.filter(and_(DefaultModel.OperatorModel.email == email, DefaultModel.OperatorModel.id != model_id)).first()
        if operator:
            return True
        return False

    def validate_and_get_operator_by(self, identifier: str, password: str):
        response: DefaultModel.OperatorModel = self.get_operator_by_identifier(identifier)
        if response and response.verify_password(password):
            return response
        return None

    def login_by_operator_model(self, operator, is_api: bool = False):
        if not operator:
            raise pffrc_exception.error_message_exception(PFFAuthMessage.INVALID_CREDENTIALS)
        if not operator.isActive:
            raise pffrc_exception.error_message_exception(PFFAuthMessage.ACCOUNT_INACTIVE)
        if not operator.isVerified:
            raise pffrc_exception.error_message_exception(PFFAuthMessage.ACCOUNT_NOT_VERIFIED)

        auth_intercept_on_verify_class = PyCommon.import_from_string(PFFAuthConfig.authInterceptOnVerifyABC, PFFAuthConfig.isStringImportSilent)
        if auth_intercept_on_verify_class and issubclass(auth_intercept_on_verify_class, AuthInterceptOnVerifyABC):
            auth_intercept = auth_intercept_on_verify_class()
            intercept_response = auth_intercept.process(operator, self, is_api)
            if intercept_response:
                return intercept_response

        return operator

    def login_operator(self, identifier: str, password: str, is_api: bool = False):
        operator: DefaultModel.OperatorModel = None
        auth_custom_login_class = PyCommon.import_from_string(PFFAuthConfig.authCustomLoginABC, PFFAuthConfig.isStringImportSilent)
        if auth_custom_login_class and issubclass(auth_custom_login_class, AuthCustomLoginABC):
            custom_login = auth_custom_login_class()
            operator = custom_login.process(identifier, password, is_api, self)
        else:
            operator = self.validate_and_get_operator_by(identifier, password)
        return self.login_by_operator_model(operator, is_api)

    def forgot_password(self, email: str, is_api: bool = False):
        operator = self.get_operator_by_email(email)
        if operator:
            self.send_forgot_password_email(operator, is_api)
        return True

    def send_forgot_password_email(self, operator: DefaultModel.OperatorModel, is_api: bool = False):
        operator.token = PyCommon.get_random() + str(operator.id)
        validity = self.jwt_helper.get_token_validity(PFFAuthConfig.resetPasswordTokenValidMin)
        token = self.jwt_helper.get_token(validity, {"token": operator.token})
        operator.save()
        self.operator_email_service.forgot_password_email(token, operator, is_api)

    def rest_password_by_token(self, token: str, new_password: str):
        payload = self.jwt_helper.validate_token(token)
        if payload and "token" in payload:
            operator: DefaultModel.OperatorModel = self.get_operator_by_token(payload["token"])
            if operator:
                operator.password = new_password
                operator.token = None
                operator.save()
                return True
        return False

    def is_valid_rest_password_token(self, token: str) -> bool:
        payload = self.jwt_helper.validate_token(token)
        if payload:
            operator: DefaultModel.OperatorModel = self.get_operator_by_token(payload["token"])
            if operator:
                return True
        return False
