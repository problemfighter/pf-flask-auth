from abc import abstractmethod
from pf_flask_rest.api.pf_app_api_def import APIPrimeDef


class AuthMethodsAbc:

    @abstractmethod
    def login(self, definition: APIPrimeDef = None):
        pass

    @abstractmethod
    def change_password(self):
        pass

    @abstractmethod
    def reset_password(self, definition: APIPrimeDef = None):
        pass

    @abstractmethod
    def forgot_password(self, definition: APIPrimeDef = None):
        pass
