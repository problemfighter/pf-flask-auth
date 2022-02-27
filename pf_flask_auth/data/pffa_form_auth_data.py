from pf_flask_auth.common.pffa_session_man import SessionMan


class FormAuthData(object):
    _SESSION_KEY = "AUTH_DETAILS"
    isLoggedIn: bool = False
    firstName: str = None
    lastName: str = None
    name: str = None
    email: str = None
    username: str = None
    id: int = None
    uuid: str = None
    otherFields: dict = {}

    def login_success(self, operator):
        self.isLoggedIn = True
        self._serialize(operator)
        SessionMan.add(self._SESSION_KEY, self.__dict__)

    def get_logged_in_session(self):
        self._deserialize()
        return self

    @staticmethod
    def ins():
        return FormAuthData()

    def _serialize(self, operator):
        for field in dir(self):
            if not field.startswith('_') and hasattr(operator, field):
                setattr(self, field, getattr(operator, field))

        for field in operator.__dict__:
            if not field.startswith('_') and field not in ["password"] and not hasattr(self, field):
                self.otherFields[field] = getattr(operator, field)

    def _deserialize(self):
        data = SessionMan.get(self._SESSION_KEY)
        if data:
            for field in data:
                setattr(self, field, data[field])
