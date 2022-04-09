from pf_flask_auth.common.pffa_auth_const import PFFAuthConst
from pf_flask_auth.dto.default_dto import OperatorDTO
from pf_flask_auth.model.pffa_abstract_model import OperatorAbstract, OperatorTokenAbstract
from pf_flask_mail.common.pffm_config import PFFMConfig


class PFFAuthConfig(object):
    loginIdentifier: str = PFFAuthConst.EMAIL
    skipUrlList: list = [
        "/",
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
    loginViewName = "PF Flask Auth"
    formUrlPrefix = "/auth"
    apiURLStartWith = "/api"
    apiUrlPrefix = "/api/v1/operator"
    successRedirect = "/dashboard"

    loginURL = "/login"
    resetPasswordURL = "/reset-password"
    forgotPasswordURL = "/forgot-password"
    renewTokenURL = "/renew-token"
    logoutURL = "/logout"

    enablePFAPIConvention: bool = True

    # JWT
    jwtRefreshTokenValidityMin: int = 45
    jwtAccessTokenValidityMin: int = 30
    jwtSecret: str = "PleaseChangeTheToken"
    resetPasswordTokenValidMin: int = 150

    # Extension
    customOperatorDTO: OperatorDTO = OperatorDTO

    # Model Customization
    isCreateDefaultModel: bool = True
    customOperatorModel: OperatorAbstract = None
    customOperatorTokenModel: OperatorTokenAbstract = None

    operatorAdditionalFields: list = None  # {"name": "name", "defaultValue": "defaultValue"}

    # Interceptor
    isStringImportSilent: bool = True
    authInterceptOnVerifyABC: str = None
    authInterceptAPILoginTokenABC: str = None
    authInterceptRenewTokenABC: str = None
    authInterceptOnAclABC: str = None
    authCustomLoginABC: str = None

    # Email Configuration
    emailConfig: PFFMConfig = None
    emailFormAppBaseURL: str = ""
    emailRestAppBaseURL: str = ""
    emailTemplatePath: str = None

