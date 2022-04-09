from abc import ABC, abstractmethod
from pf_flask_auth.data.pffa_form_auth_data import FormAuthData
from pf_flask_auth.model.pffa_default_model import DefaultModel
from pf_flask_rest_com.data.pffrc_request_info import PFFRCRequestInfo


class AuthInterceptOnVerifyABC(ABC):

    @abstractmethod
    def process(self, operator: DefaultModel.OperatorModel, operator_service, is_api: bool) -> DefaultModel.OperatorModel:
        pass


class AuthInterceptAPILoginTokenABC(ABC):

    @abstractmethod
    def process(self, response_map: dict, operator: DefaultModel.OperatorModel, operator_api_service) -> dict:
        pass


class AuthInterceptRenewTokenABC(ABC):

    @abstractmethod
    def process(self, response_map: dict, requested_jwt_payload: dict, operator_api_service) -> dict:
        pass


class AuthInterceptOnAclABC(ABC):

    @abstractmethod
    def process(self, url_info: PFFRCRequestInfo, payload: dict = None, form_auth_data: FormAuthData = None, is_api: bool = False):
        pass


class AuthCustomLoginABC(ABC):

    @abstractmethod
    def process(self, identifier: str, password: str, is_api: bool, operator_service) -> DefaultModel.OperatorModel:
        pass
