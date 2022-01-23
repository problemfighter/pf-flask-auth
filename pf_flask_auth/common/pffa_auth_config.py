from pf_flask_auth.data.pffa_extend_data import OperatorExtend, OperatorDTOExtend


class PFFAuthConfig(object):
    operatorExtend: OperatorExtend = OperatorExtend
    operatorDTOExtend: OperatorDTOExtend = OperatorDTOExtend
    jwtRefreshTokenValidityMin: str = None
    jwtAccessTokenValidityMin: str = None
    jwtSecret: str = None
    enableAPIAuth: bool = True
    enableSessionAuth: bool = False
    skipUrlList: list = [
        "/"
    ]

    skipStartWithUrlList: list = [
        "/favicon.ico",
        "/static/"
    ]
