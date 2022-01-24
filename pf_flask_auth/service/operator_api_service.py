from pf_flask_auth.common.pffa_jwt_helper import JWTHelper
from pf_flask_auth.service.operator_service import OperatorService


class OperatorAPIService:
    operator_service: OperatorService = OperatorService()
    jwt_helper = JWTHelper()
