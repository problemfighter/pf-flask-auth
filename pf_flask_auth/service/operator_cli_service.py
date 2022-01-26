from pf_flask_auth.common.pffa_auth_message import PFFAuthMessage
from pf_flask_auth.dto.operator_dto import CreateCLIOperatorDTO
from pf_flask_auth.service.operator_service import OperatorService
from pf_flask_rest.pf_flask_request_processor import RequestProcessor


class OperatorCLIService:
    operator_service: OperatorService = OperatorService()
    request_processor: RequestProcessor = RequestProcessor()

    def create_operator_by_email(self, data: dict):
        try:
            self.request_processor.validate_data(data, CreateCLIOperatorDTO())
            self.operator_service.create_operator_by_email(data["email"], data["password"])
            return PFFAuthMessage.OPERATOR_CREATED
        except Exception as e:
            return str(e)

    def change_password(self):
        pass

    def reset_password(self):
        pass

    def forgot_password(self):
        pass


operator_cli_service = OperatorCLIService()
