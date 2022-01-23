from pf_flask_auth.common.pffa_jwt_helper import jwt_helper
from pf_flask_rest_com.pf_flask_request_helper import request_helper


class AuthUtil:

    @staticmethod
    def get_api_auth_data():
        bearer_token = request_helper.get_bearer_token()
        return jwt_helper.validate_token(bearer_token)
