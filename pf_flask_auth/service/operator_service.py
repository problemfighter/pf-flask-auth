from sqlalchemy import and_
from pf_flask_auth.common.pffa_auth_config import PFFAuthConfig
from pf_flask_auth.common.pffa_auth_const import PFFAuthConst
from pf_flask_auth.common.pffa_auth_interceptor_abc import AuthInterceptOnVerifyABC
from pf_flask_auth.common.pffa_auth_message import PFFAuthMessage
from pf_flask_auth.model.operator import Operator
from pf_flask_rest_com.common.pffr_exception import pffrc_exception
from pf_py_common.py_common import PyCommon


class OperatorService:

    def get_operator_by_email(self, email):
        return Operator.query.filter(Operator.email == email, Operator.isDeleted == False).first()

    def get_operator_by_username(self, username):
        return Operator.query.filter(and_(Operator.username == username, Operator.isDeleted == False)).first()

    def get_operator_by_id(self, model_id):
        return Operator.query.filter(and_(Operator.id == model_id, Operator.isDeleted == False)).first()

    def get_operator_by_identifier(self, identifier):
        if PFFAuthConfig.loginIdentifier == PFFAuthConst.USERNAME:
            return self.get_operator_by_username(identifier)
        else:
            return self.get_operator_by_email(identifier)

    def create_operator_by_email(self, email, password):
        operator = self.get_operator_by_email(email)
        if operator:
            raise pffrc_exception.error_message_exception(PFFAuthMessage.OPERATOR_EXIST)

        operator = Operator()
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
        operator = Operator.query.filter(and_(Operator.email == email, Operator.id != model_id)).first()
        if operator:
            return True
        return False

    def validate_and_get_operator_by(self, identifier: str, password: str):
        response: Operator = self.get_operator_by_identifier(identifier)
        if response and response.verify_password(password):
            return response
        return None

    def login_operator(self, identifier: str, password: str, is_api: bool = False):
        operator: Operator = self.validate_and_get_operator_by(identifier, password)
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
