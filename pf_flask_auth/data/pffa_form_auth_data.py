from pf_flask_auth.model.operator import Operator


class FormAuthData(object):
    isLoggedIn: bool = False
    operator: Operator = None
