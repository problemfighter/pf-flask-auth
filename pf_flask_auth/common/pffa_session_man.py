from flask import session


class SessionMan:
    autoPrefix = "pfa_"

    @staticmethod
    def add(key: str, value):
        session[SessionMan.autoPrefix + key] = value

    @staticmethod
    def get(key: str, default=None):
        store_key = SessionMan.autoPrefix + key
        if store_key in session:
            return session[store_key]
        return default

    @staticmethod
    def remove(key: str):
        store_key = SessionMan.autoPrefix + key
        session.pop(store_key)

    @staticmethod
    def destroy():
        session.clear()

    @staticmethod
    def all(default=None):
        key_values = {}
        for item in session:
            key = str(item)
            if key and key.startswith(SessionMan.autoPrefix):
                key_values[key[len(SessionMan.autoPrefix):]] = session[key]
        if key_values:
            return key_values
        return default
