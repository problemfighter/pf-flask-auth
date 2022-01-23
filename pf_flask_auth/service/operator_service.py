from pf_flask_auth.model.operator import Operator
from sqlalchemy import and_
from pf_flask_auth.common.pffa_jwt_helper import JWTHelper


class OperatorService:
    jwt_helper = JWTHelper()

    def get_operator_by_email(self, email):
        return Operator.query.filter(Operator.email == email).first()

    def get_operator_by_username(self, username):
        return Operator.query.filter(Operator.username == username).first()

    def get_operator_by_id(self, id):
        return Operator.query.filter(and_(Operator.id == id, Operator.isDeleted == False)).first()

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

    def init_default_operator(self):
        email = get_global_app_config().LOGIN_DEFAULT_EMAIL
        password = get_global_app_config().LOGIN_DEFAULT_PASSWORD
        operator = self.create_operator_by_email(email, password)
        if operator:
            return True
        return False

    def login_by(self, identifier, password):
        response: Operator
        if get_global_app_config().LOGIN_IDENTIFIER == "username":
            response = self.get_operator_by_username(identifier)
        else:
            response = self.get_operator_by_email(identifier)
        if response and response.verify_password(password):
            return response
        return None

    def login_operator(self):
        login_credential = self.json_request_process(LoginDto())
        response = self.login_by(login_credential['identifier'], login_credential['password'])
        if not response:
            return self.error("Invalid Credentials! Please enter valid Credential")
        if not response.isActive:
            return self.error("Sorry your account has been inactive.")
        if not response.isVerified:
            return self.error("Sorry your account has not been verified.")
        if response.isDeleted:
            return self.error("Invalid Access Credentials!")
        return self.process_login_response(response)

    def process_login_response(self, operator):
        operator_details = OperatorDto().dump(operator)
        response_map: dict = {
            "operator": operator_details
        }
        login_token: dict = {}
        error_message = "Unable to process login request"
        access_token = self.get_access_token(operator.id)
        if not access_token:
            return self.error(error_message)
        login_token['accessToken'] = access_token
        refresh_token = self.get_refresh_token(operator.id)
        if not refresh_token:
            return self.error(error_message)
        login_token['refreshToken'] = refresh_token
        response_map["loginToken"] = login_token

        auth_processor_class = import_from_string(get_global_app_config().AUTH_PROCESSOR,
                                                  get_global_app_config().STRING_IMPORT_SILENT)
        if auth_processor_class and issubclass(auth_processor_class, AuthProcessorABC):
            auth_processor = auth_processor_class()
            response = auth_processor.process(response_map, operator, self)
            if response:
                return self.json_list_dic_data_response(response)
        return self.json_list_dic_data_response(response_map)

    def get_access_token(self, operator_id, payload: dict = None):
        operator = self.get_operator_by_id(operator_id)
        if not operator:
            return None

        if not payload:
            payload = {}
        payload["operator"] = operator.id
        return self.jwt_helper.get_access_token(payload, iss=operator.uuid)

    def get_refresh_token(self, operator_id, payload: dict = None):
        operator = self.get_operator_by_id(operator_id)
        if not operator:
            return None
        if not payload:
            payload = {}
        payload["operator"] = operator.id
        db_token = self.create_or_update_db_refresh_token(operator_id)
        if not db_token:
            return None
        payload['token'] = db_token.token
        return self.jwt_helper.get_refresh_token(payload, iss=operator.uuid)

    def create_or_update_db_refresh_token(self, operator_id, uuid=None):
        existing_token: OperatorToken = self.get_operator_token_by_operator_id(operator_id)
        if uuid:
            if not existing_token or existing_token.token != uuid:
                return None
        else:
            if not existing_token:
                existing_token = OperatorToken(name="REFRESH_TOKEN", operatorId=operator_id)
        existing_token.token = get_uuid()
        self.crud_service.save(existing_token)
        return existing_token

    def get_operator_token_by_operator_id(self, operator_id):
        return OperatorToken.query.filter(OperatorToken.operatorId == operator_id).first()

    def get_operator_token_by_token(self, token):
        return OperatorToken.query.filter(OperatorToken.token == token).first()

    def renew_token(self):
        login_credential = self.json_request_process(RefreshTokenDto())
        jwt_payload = self.jwt_helper.validate_token(login_credential['refreshToken'])
        if not jwt_payload:
            return self.error("Invalid Token", 5500)
        if "token" not in jwt_payload or "operator" not in jwt_payload:
            return self.error("Invalid Token", 5500)
        operator_token = self.get_operator_token_by_token(jwt_payload["token"])
        operator_id = jwt_payload["operator"]
        if not operator_token:
            return self.error("Token Expired", 5501)

        access_token = self.get_access_token(operator_id)
        refresh_token = self.get_refresh_token(operator_id)
        if not access_token or not refresh_token:
            return self.error("Unable to generate token", 5502)

        response_map = {
            "loginToken": {
                "accessToken": access_token,
                "refreshToken": refresh_token,
            }
        }

        refresh_token_processor_class = import_from_string(get_global_app_config().AUTH_REFRESH_TOKEN_PROCESSOR,
                                                           get_global_app_config().STRING_IMPORT_SILENT)
        if refresh_token_processor_class and issubclass(refresh_token_processor_class, AuthRefreshTokenProcessorABC):
            refresh_token_processor = refresh_token_processor_class()
            response = refresh_token_processor.process(response_map, jwt_payload, self)
            if response:
                return self.json_list_dic_data_response(response)
        return self.json_list_dic_data_response(response_map)

    def is_operator_email_exist(self, email):
        if self.get_operator_by_email(email):
            return True
        return False

    def is_other_operator_email_exist(self, email, id):
        operator = Operator.query.filter(and_(Operator.email == email, Operator.id != id)).first()
        if operator:
            return True
        return False


operator_service = OperatorService()
