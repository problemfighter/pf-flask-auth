from fpf_common.common.pff_request_header_helper import pff_request_header_helper
from pf_auth.common.jwt_helper import JWTHelper
from pf_flask.global_registry import get_global_app_config
from pf_flask.pff_utils import import_from_string
from pf_fr.interface.auth_acl_processor_abc import AuthACLProcessorABC
from pfms.pfapi.rr.pfms_request_respons import PfRequestResponse

SYSTEM_DEFAULT_SKIP_URL = [
    "/",
    "/api/v1/operator/renew-token",
    "/pf-swagger-ui",
    "/api/v1/operator/login",
    "/api/v1/operator/init",
    "/pf-swagger-json"
]

SYSTEM_DEFAULT_SKIP_START_WITH_URL = [
    "/favicon.ico",
    "/pf-marshmallow-swagger/",
    "/static/"
]


class AuthInterceptor(PfRequestResponse):

    jwt_helper = JWTHelper()


    def intercept(self):
        url_info = pff_request_header_helper.get_url_info()
        if url_info['method'] == 'OPTIONS':
            return self.success("Allowed")
        relative_url = url_info['relative_url']
        if not relative_url:
            relative_url = url_info["relative_url_with_param"]
        skip_urls = SYSTEM_DEFAULT_SKIP_URL
        if get_global_app_config() and get_global_app_config().SKIP_URL_ON_AUTH:
            skip_urls += get_global_app_config().SKIP_URL_ON_AUTH
        if relative_url not in skip_urls and not self.check_url_start_with(relative_url):
            return self.check_auth(url_info)

    def check_url_start_with(self, request_url):
        for url in SYSTEM_DEFAULT_SKIP_START_WITH_URL:
            if request_url.startswith(url):
                return True
        return False

    def check_auth(self, url_info):
        bearer_token = pff_request_header_helper.get_bearer_token()
        if not bearer_token:
            return self.get_error_response()
        payload = self.jwt_helper.validate_token(bearer_token)
        if not payload:
            return self.get_error_response()
        return self.intercept_acl(url_info, payload)

    def get_error_response(self, message="You are not Authorize for Access."):
        return self.error(message, code=4100, http_code=401)

    def intercept_acl(self, url_info, payload):
        auth_acl_processor_class = import_from_string(get_global_app_config().AUTH_ACL_PROCESSOR, get_global_app_config().STRING_IMPORT_SILENT)
        if auth_acl_processor_class and issubclass(auth_acl_processor_class, AuthACLProcessorABC):
            auth_acl_processor = auth_acl_processor_class()
            return auth_acl_processor.process(url_info, payload, self)
        return None


auth_interceptor = AuthInterceptor()
