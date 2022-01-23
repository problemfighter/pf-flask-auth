class PFFAuthConfig(object):
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
