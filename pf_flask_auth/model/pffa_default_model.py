from pf_flask_auth.common.pffa_auth_config import PFFAuthConfig
from pf_flask_auth.model.pffa_abstract_model import OperatorAbstract, OperatorTokenAbstract


class DefaultModel:
    OperatorTokenModel: OperatorTokenAbstract = None
    OperatorModel: OperatorAbstract = None

    def init_model(self):
        if not DefaultModel.OperatorModel:
            DefaultModel.OperatorModel = self._get_operator_model()

        if not DefaultModel.OperatorTokenModel:
            DefaultModel.OperatorTokenModel = self._get_operator_token_model()


    def _get_operator_model(self):
        if not PFFAuthConfig.isCreateDefaultModel:
            return PFFAuthConfig.customOperatorModel

        class Operator(OperatorAbstract):
            pass

        return Operator


    def _get_operator_token_model(self):
        if not PFFAuthConfig.isCreateDefaultModel:
            return PFFAuthConfig.customOperatorTokenModel

        class OperatorToken(OperatorTokenAbstract):
            pass

        return OperatorToken
