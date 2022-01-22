from pf_flask.global_registry import get_global_app_config
import datetime
import jwt


class JWTHelper:
    ALGORITHMS: str = "HS256"

    def get_token(self, exp: datetime, payload: dict = None, iss=None):
        if not payload:
            payload = {}
        payload["exp"] = exp
        if iss:
            payload["iss"] = iss
        return jwt.encode(payload, get_global_app_config().JWT_SECRET, algorithm=self.ALGORITHMS)

    def get_access_token(self, payload: dict = None, iss=None):
        validity = self.get_access_token_validity()
        return self.get_token(validity, payload=payload, iss=iss)

    def get_refresh_token(self, payload: dict = None, iss=None):
        validity = self.get_refresh_token_validity()
        return self.get_token(validity, payload=payload, iss=iss)

    def validate_token(self, token: str):
        try:
            if not token:
                return None
            return jwt.decode(token, get_global_app_config().JWT_SECRET, algorithms=[self.ALGORITHMS])
        except:
            return None

    def get_access_token_validity(self, minutes=None):
        if not minutes:
            minutes = get_global_app_config().JWT_ACCESS_TOKEN_VALIDITY_MIN
        return self.get_token_validity(minutes)

    def get_refresh_token_validity(self, minutes=None):
        if not minutes:
            minutes = get_global_app_config().JWT_REFRESH_TOKEN_VALIDITY_MIN
        return self.get_token_validity(minutes)

    def get_token_validity(self, minutes):
        return datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=minutes)


jwt_helper = JWTHelper()
