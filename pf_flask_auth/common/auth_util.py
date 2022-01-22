from fpf_common.common.pff_request_header_helper import pff_request_header_helper
from pf_auth.common.jwt_helper import jwt_helper


def get_current_operator_payload():
    bearer_token = pff_request_header_helper.get_bearer_token()
    return jwt_helper.validate_token(bearer_token)
