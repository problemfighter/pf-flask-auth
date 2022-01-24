from sqlalchemy import and_
from pf_flask_auth.common.pffa_auth_config import PFFAuthConfig
from pf_flask_auth.common.pffa_auth_const import PFFAuthConst
from pf_flask_auth.model.operator import Operator


class OperatorService:

    def get_operator_by_email(self, email):
        return Operator.query.filter(Operator.email == email, Operator.isDeleted == False).first()

    def get_operator_by_username(self, username):
        return Operator.query.filter(and_(Operator.username == username, Operator.isDeleted == False)).first()

    def get_operator_by_id(self, model_id):
        return Operator.query.filter(and_(Operator.id == model_id, Operator.isDeleted == False)).first()

    def get_operator_by_identifier(self, identifier):
        if PFFAuthConfig.loginIdentifier == PFFAuthConst.USERNAME:
            return self.get_operator_by_username(identifier)
        else:
            return self.get_operator_by_email(identifier)

    def create_operator_by_email(self, email, password):
        operator = self.get_operator_by_email(email)
        if not operator:
            operator = Operator()
            operator.email = email
            operator.password = password
            operator.save()
            if operator.id:
                return operator
        return None

    def is_operator_email_exist(self, email):
        if self.get_operator_by_email(email):
            return True
        return False

    def is_other_operator_email_exist(self, email, model_id):
        operator = Operator.query.filter(and_(Operator.email == email, Operator.id != model_id)).first()
        if operator:
            return True
        return False

    def login_by(self, identifier, password):
        response: Operator = self.get_operator_by_identifier(identifier)
        if response and response.verify_password(password):
            return response
        return None
