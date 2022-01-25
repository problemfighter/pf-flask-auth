from pf_flask_auth.common.pffa_auth_methods_abc import AuthMethodsAbc
from pf_flask_auth.service.operator_service import OperatorService


class OperatorFormService(AuthMethodsAbc):
    operator_service: OperatorService = OperatorService()

    def login(self):
        pass

    def change_password(self):
        pass

    def reset_password(self):
        pass

    def forgot_password(self):
        pass
