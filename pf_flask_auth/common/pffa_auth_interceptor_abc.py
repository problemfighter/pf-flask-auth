from abc import ABC, abstractmethod

from pf_flask_auth.data.pffa_form_auth_data import FormAuthData
from pf_flask_auth.model.operator import Operator
from pf_flask_rest_com.data.pffrc_request_info import PFFRCRequestInfo


class AuthInterceptOnVerifyABC(ABC):

    @abstractmethod
    def process(self, operator: Operator, operator_service, is_api: bool) -> Operator:
        pass


class AuthInterceptAPILoginTokenABC(ABC):

    @abstractmethod
    def process(self, response_map: dict, operator: Operator, operator_api_service) -> dict:
        pass


class AuthInterceptRenewTokenABC(ABC):

    @abstractmethod
    def process(self, response_map: dict, requested_jwt_payload: dict, operator_api_service) -> dict:
        pass


class AuthInterceptOnAclABC(ABC):

    @abstractmethod
    def process(self, url_info: PFFRCRequestInfo, payload: dict = None, form_auth_data: FormAuthData = None, is_api: bool = False):
        pass
