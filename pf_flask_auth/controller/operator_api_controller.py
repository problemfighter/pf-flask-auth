from flask import Blueprint

from pf_flask_auth.common.pffa_auth_config import PFFAuthConfig

url_prefix = PFFAuthConfig.api_url_prefix
operator_api_controller = Blueprint("operator_api_controller", __name__, url_prefix=url_prefix)
