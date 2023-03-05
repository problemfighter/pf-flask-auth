import enum
import json
from datetime import datetime
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
    profilePhoto: str = None
    coverPhoto: str = None
    otherFields: dict = {}
    _otherFields: str = None

    def login_success(self, operator):
        self.update_data(operator)

    def get_logged_in_session(self):
        self._deserialize()
        return self

    def update_data(self, operator):
        self.isLoggedIn = True
        self._serialize(operator)
        SessionMan.add(self._SESSION_KEY, self.__dict__)

    @staticmethod
    def ins():
        return FormAuthData()

    def _serialize(self, operator):
        for field in dir(self):
            if not field.startswith('_') and hasattr(operator, field):
                setattr(self, field, getattr(operator, field))

        for field in operator.__dict__:
            if not field.startswith('_') and field not in ["password", "password_hash"] and not hasattr(self, field):
                data = getattr(operator, field)
                if isinstance(data, enum.Enum) or isinstance(data, datetime):
                    data = str(data)
                self.otherFields[field] = data
        self._otherFields = json.dumps(self.otherFields)

    def _deserialize(self):
        data = SessionMan.get(self._SESSION_KEY)
        if data:
            for field in data:
                setattr(self, field, data[field])
            if "_otherFields" in data:
                self.otherFields = json.loads(data["_otherFields"])
