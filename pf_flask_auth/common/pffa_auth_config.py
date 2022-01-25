from pf_flask_auth.data.pffa_extend_data import OperatorExtend, OperatorDTOExtend


class PFFAuthConfig(object):
    loginIdentifier: str = "email"
    skipUrlList: list = [
        "/"
    ]

    skipStartWithUrlList: list = [
        "/favicon.ico",
        "/static/"
    ]

    # Functionality
    enableAPIAuth: bool = False
    enableSessionAuth: bool = True
    enableAPIEndPoints: bool = False
    enableFormEndPoints: bool = True

    # EndPoints
    form_url_prefix = "/auth"
    api_url_prefix = "/api/v1/operator"

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
