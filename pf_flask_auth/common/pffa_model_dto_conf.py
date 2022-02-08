from pf_flask_auth.dto.operator_dto import OperatorDTO
from pf_flask_auth.model.operator import Operator
from pf_flask_auth.model.operator_token import OperatorToken


class PFFAModelDTOConf:
    OperatorModel: Operator = Operator
    OperatorTokenModel: OperatorToken = OperatorToken

    OperatorDTODefault: OperatorDTO = OperatorDTO
