from pf_flask_auth.common.pffa_auth_interceptor_abc import AuthInterceptOnVerifyABC
from pf_flask_auth.data.pffa_extend_data import OperatorExtend, OperatorDTOExtend


class PFFAuthConfig(object):
    loginIdentifier: str = "email"
    enableAPIAuth: bool = True
    enableSessionAuth: bool = False
    skipUrlList: list = [
        "/"
    ]

    skipStartWithUrlList: list = [
        "/favicon.ico",
        "/static/"
    ]

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
