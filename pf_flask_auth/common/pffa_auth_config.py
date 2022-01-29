from pf_flask_auth.common.pffa_auth_const import PFFAuthConst
from pf_flask_auth.data.pffa_extend_data import OperatorExtend, OperatorDTOExtend


class PFFAuthConfig(object):
    loginIdentifier: str = PFFAuthConst.EMAIL
    skipUrlList: list = [
        "/"
    ]

    skipStartWithUrlList: list = [
        "/favicon.ico",
        "/static/",
    ]

    # Functionality
    enableAPIAuth: bool = False
    enableSessionAuth: bool = True
    enableAPIEndPoints: bool = False
    enableFormEndPoints: bool = True

    # End Points
    formUrlPrefix = "/auth"
    apiUrlPrefix = "/api/v1/operator"
    loginViewName = "PF Flask Auth"
    successRedirect = "/dashboard"
    apiURLStartWith = "/api"

    loginURL = "/login"
    resetPasswordURL = "/reset-password"
    forgotPasswordURL = "/forgot-password"

    # JWT
    jwtRefreshTokenValidityMin: str = None
    jwtAccessTokenValidityMin: str = None
    jwtSecret: str = None

    # Extension
    operatorExtend: OperatorExtend = OperatorExtend
    operatorDTOExtend: OperatorDTOExtend = OperatorDTOExtend

    # Interceptor
    isStringImportSilent: bool = True
    authInterceptOnVerifyABC: str = None
    authInterceptAPILoginTokenABC: str = None
    authInterceptRenewTokenABC: str = None
    authInterceptOnAclABC: str = None
