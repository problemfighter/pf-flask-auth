from pf_flask_auth.common.pffa_auth_config import PFFAuthConfig
from pf_flask_auth.common.pffa_auth_const import PFFAuthConst
from pf_flask_auth.common.pffa_auth_interceptor_abc import AuthInterceptAPILoginTokenABC, AuthInterceptRenewTokenABC
from pf_flask_auth.common.pffa_auth_message import PFFAuthMessage
from pf_flask_auth.common.pffa_auth_methods_abc import AuthMethodsAbc
from pf_flask_auth.dto.operator_dto import OperatorDTO, LoginDTO, ForgotPasswordDTO, ResetPasswordDTO, RefreshTokenDTO
from pf_flask_auth.common.pffa_jwt_helper import JWTHelper
from pf_flask_auth.model.pffa_default_model import DefaultModel
from pf_flask_auth.service.operator_service import OperatorService
from pf_flask_rest.api.pf_app_api_def import APIPrimeDef
from pf_flask_rest.pf_flask_request_processor import RequestProcessor
from pf_flask_rest.pf_flask_response_processor import ResponseProcessor
from pf_flask_rest_com.common.pffr_exception import pffrc_exception
from pf_flask_rest_com.data.pffrc_response_data import PFFRCDataResponse
from pf_flask_rest_com.data.pffrc_response_status import PFFRCResponseStatus, PFFRCResponseCode, PFFRCHTTPCode
from pf_py_common.py_common import PyCommon


class OperatorAPIService(AuthMethodsAbc):
    _token = "token"
    _access_token = "accessToken"
    _refresh_token = "refreshToken"
    _login_token = "loginToken"
    _operator = "operator"

    operator_service: OperatorService = OperatorService()
    jwt_helper = JWTHelper()
    request_processor = RequestProcessor()
    response_processor = ResponseProcessor()

    def _data_response(self, data):
        if not PFFAuthConfig.enablePFAPIConvention:
            return self.response_processor.response_helper.json_response(data)
        return self.response_processor.dict_response(data)

    def login(self, definition: LoginDTO = None):
        data = self.request_processor.get_rest_json_data(LoginDTO())
        operator: DefaultModel.OperatorModel = self.operator_service.login_operator(data["identifier"], data["password"], True)
        processed_response = self.process_login_response(operator)
        return self._data_response(processed_response)

    def reset_password(self, definition: ResetPasswordDTO = None):
        data = self.request_processor.get_rest_json_data(ResetPasswordDTO())
        is_success = self.operator_service.rest_password_by_token(data["token"], data["newPassword"])
        if is_success:
            return self.response_processor.success_message(PFFAuthMessage.PASS_RESET_SUCCESS)
        return self.response_processor.error_message(PFFAuthMessage.INVALID_TOKEN_OR_EXPIRE)

    def forgot_password(self, definition: APIPrimeDef = None):
        data = self.request_processor.get_rest_json_data(ForgotPasswordDTO())
        self.operator_service.forgot_password(data["email"])
        return self.response_processor.success_message(PFFAuthMessage.PASS_RESET_REQUEST)

    def logout(self):
        return self.response_processor.success_message(PFFAuthMessage.LOGOUT_SUCCESS)

    def renew_token(self):
        data = self.request_processor.get_rest_json_data(RefreshTokenDTO())
        response = self.renew_token_by_refresh_token(data["refreshToken"])
        return self._data_response(response)

    def process_login_response(self, operator: DefaultModel.OperatorModel) -> dict:
        operator_details = OperatorDTO().dump(operator)
        response_map: dict = {
            self._operator: operator_details
        }
        login_token: dict = {}
        error_message = PFFAuthMessage.ERROR_ON_TOKEN_CREATION
        access_token = self.get_access_token(operator.id)
        if not access_token:
            raise pffrc_exception.error_message_exception(error_message)
        login_token[self._access_token] = access_token
        refresh_token = self.get_refresh_token(operator.id)
        if not refresh_token:
            raise pffrc_exception.error_message_exception(error_message)
        login_token[self._refresh_token] = refresh_token
        response_map[self._login_token] = login_token

        intercept_class = PyCommon.import_from_string(PFFAuthConfig.authInterceptAPILoginTokenABC, PFFAuthConfig.isStringImportSilent)
        if intercept_class and issubclass(intercept_class, AuthInterceptAPILoginTokenABC):
            auth_intercept = intercept_class()
            intercept_response = auth_intercept.process(response_map, operator, self)
            if intercept_response:
                return intercept_response
        return response_map

    def get_access_token(self, operator_id, payload: dict = None):
        operator = self.operator_service.get_operator_by_id(operator_id)
        if not operator:
            return None

        if not payload:
            payload = {}
        payload[self._operator] = operator.id
        return self.jwt_helper.get_access_token(payload, iss=operator.uuid)

    def get_refresh_token(self, operator_id, payload: dict = None):
        operator = self.operator_service.get_operator_by_id(operator_id)
        if not operator:
            return None
        if not payload:
            payload = {}
        payload[self._operator] = operator.id
        db_token = self.create_or_update_db_refresh_token(operator_id)
        if not db_token:
            return None
        payload[self._token] = db_token.token
        return self.jwt_helper.get_refresh_token(payload, iss=operator.uuid)


    def get_operator_token_by_operator_id(self, operator_id):
        return DefaultModel.OperatorTokenModel.query.filter(DefaultModel.OperatorTokenModel.tokenOwnerId == operator_id).first()

    def get_operator_token_by_token(self, token):
        return DefaultModel.OperatorTokenModel.query.filter(DefaultModel.OperatorTokenModel.token == token).first()

    def create_or_update_db_refresh_token(self, operator_id, uuid=None):
        existing_token: DefaultModel.OperatorTokenModel = self.get_operator_token_by_operator_id(operator_id)
        if uuid and (not existing_token or existing_token.token != uuid):
            return None
        if not existing_token:
            existing_token = DefaultModel.OperatorTokenModel(name=PFFAuthConst.REFRESH_TOKEN_NAME, tokenOwnerId=operator_id)

        existing_token.token = PyCommon.uuid()
        existing_token.save()
        return existing_token

    def renew_token_by_refresh_token(self, token):
        jwt_payload = self.jwt_helper.validate_token(token)
        if not jwt_payload:
            raise pffrc_exception.error_message_exception(PFFAuthMessage.INVALID_TOKEN, PFFAuthConst.INVALID_TOKEN_CODE)
        if self._token not in jwt_payload or self._operator not in jwt_payload:
            raise pffrc_exception.error_message_exception(PFFAuthMessage.INVALID_TOKEN, PFFAuthConst.INVALID_TOKEN_CODE)

        operator_token = self.get_operator_token_by_token(jwt_payload[self._token])
        operator_id = jwt_payload[self._operator]
        if not operator_token:
            raise pffrc_exception.error_message_exception(PFFAuthMessage.TOKEN_EXPIRED, PFFAuthConst.TOKEN_EXPIRED_CODE)

        access_token = self.get_access_token(operator_id)
        refresh_token = self.get_refresh_token(operator_id)
        if not access_token or not refresh_token:
            raise pffrc_exception.error_message_exception(PFFAuthMessage.TOKEN_GENERATION_ERROR, PFFAuthConst.TOKEN_ERROR_CODE)

        response_map = {
            self._login_token: {
                self._access_token: access_token,
                self._refresh_token: refresh_token,
            }
        }

        intercept_class = PyCommon.import_from_string(PFFAuthConfig.authInterceptRenewTokenABC, PFFAuthConfig.isStringImportSilent)
        if intercept_class and issubclass(intercept_class, AuthInterceptRenewTokenABC):
            auth_intercept = intercept_class()
            intercept_response = auth_intercept.process(response_map, jwt_payload, self)
            if intercept_response:
                return intercept_response
        return response_map
