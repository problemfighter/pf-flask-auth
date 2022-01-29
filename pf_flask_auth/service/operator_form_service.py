from pf_flask_auth.common.pffa_auth_methods_abc import AuthMethodsAbc
from pf_flask_auth.common.pffa_session_man import SessionMan
from pf_flask_auth.data.pffa_form_auth_data import FormAuthData
from pf_flask_auth.dto.operator_dto import LoginFormDTO
from pf_flask_auth.service.operator_service import OperatorService


class OperatorFormService(AuthMethodsAbc):
    operator_service: OperatorService = OperatorService()

    def login(self, form_def: LoginFormDTO = None):
        try:
            operator = self.operator_service.login_operator(form_def.identifier, form_def.password, False)
            FormAuthData.ins().login_success(operator)
            return True
        except Exception as e:
            form_def.definition.add_validation_error(str(e))
        return False

    def change_password(self):
        pass

    def reset_password(self):
        pass

    def forgot_password(self):
        pass

    def logout(self):
        SessionMan.destroy()
