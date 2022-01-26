from pf_flask_auth.common.pffa_auth_methods_abc import AuthMethodsAbc
from pf_flask_auth.service.operator_service import OperatorService
from pf_flask_rest.form.pf_app_form_def import FormBaseDef


class OperatorFormService(AuthMethodsAbc):
    operator_service: OperatorService = OperatorService()

    def login(self, form_def: FormBaseDef = None):
        form_def.definition.add_validation_error("Validation Errors")
        return False

    def change_password(self):
        pass

    def reset_password(self):
        pass

    def forgot_password(self):
        pass
