from abc import ABC, abstractmethod
from pf_flask_auth.model.operator import Operator


class AuthInterceptOnVerifyABC(ABC):

    @abstractmethod
    def process(self, operator: Operator, operator_service, is_api: bool) -> Operator:
        pass
