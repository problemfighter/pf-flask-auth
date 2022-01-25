from abc import ABC, abstractmethod
from pf_flask_auth.model.operator import Operator


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
    def process(self, response_map: dict, requested_jwt_payload: dict, operator_api_service) -> Operator:
        pass


class AuthInterceptOnAclABC(ABC):

    @abstractmethod
    def process(self, operator: Operator, operator_service, is_api: bool) -> Operator:
        pass
