from pf_flask_auth.common.pffa_auth_config import PFFAuthConfig
from pf_flask_auth.common.pffa_auth_interceptor_abc import AuthInterceptOnAclABC
from pf_flask_auth.common.pffa_auth_message import PFFAuthMessage
from pf_flask_auth.common.pffa_jwt_helper import JWTHelper
from pf_flask_auth.data.pffa_form_auth_data import FormAuthData
from pf_flask_rest.pf_flask_response_processor import ResponseProcessor
from pf_flask_rest_com.data.pffrc_request_info import PFFRCRequestInfo
from pf_flask_rest_com.pf_flask_request_helper import RequestHelper
from pf_py_common.py_common import PyCommon


class AuthInterceptorService:
    jwt_helper = JWTHelper()
    request_helper = RequestHelper()
    url_info: PFFRCRequestInfo = None
    response_processor: ResponseProcessor = ResponseProcessor()

    def call_acl_interceptor(self, payload, form_auth_data: FormAuthData = None, is_api: bool = False):
        intercept_class = PyCommon.import_from_string(PFFAuthConfig.authInterceptOnAclABC, PFFAuthConfig.isStringImportSilent)
        if intercept_class and issubclass(intercept_class, AuthInterceptOnAclABC):
            auth_intercept = intercept_class()
            intercept_response = auth_intercept.process(self.url_info, payload, form_auth_data, is_api)
            if intercept_response:
                return intercept_response
        return None

    def get_relative_url(self):
        relative_url = self.url_info.relativeURL
        if not relative_url:
            relative_url = self.url_info.relativeURLWithParam
        return relative_url

    def is_rest_request(self) -> bool:
        relative_url = self.get_relative_url()
        if relative_url.startswith(PFFAuthConfig.apiURLStartWith):
            return True
        return False

    def check_url_start_with(self, request_url):
        for url in PFFAuthConfig.skipStartWithUrlList:
            if request_url.startswith(url):
                return True
        return False

    def is_listed_in_skip_url(self) -> bool:
        relative_url = self.get_relative_url()
        if relative_url in PFFAuthConfig.skipUrlList or self.check_url_start_with(relative_url):
            return True
        return False

    def get_error_response(self, message=PFFAuthMessage.NOT_AUTHORIZE):
        return self.response_processor.error_message(message, "4100", 401)

    def check_rest_auth(self):
        bearer_token = self.request_helper.get_bearer_token()
        if not bearer_token:
            return self.get_error_response()
        payload = self.jwt_helper.validate_token(bearer_token)
        if not payload:
            return self.get_error_response()
        return self.call_acl_interceptor(payload=payload, is_api=True)

    def check_form_auth(self):
        pass

    def check_auth(self):
        if self.is_rest_request():
            return self.check_rest_auth()
        else:
            return self.check_form_auth()

    def intercept(self):
        self.url_info = self.request_helper.get_url_info()
        if self.url_info.method == 'OPTIONS':
            return self.response_processor.success_message("Allowed")

        if not self.is_listed_in_skip_url():
            return self.check_auth()

