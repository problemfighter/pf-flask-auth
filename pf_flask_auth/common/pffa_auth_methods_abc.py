from abc import abstractmethod


class AuthMethodsAbc:

    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def change_password(self):
        pass

    @abstractmethod
    def reset_password(self):
        pass

    @abstractmethod
    def forgot_password(self):
        pass
