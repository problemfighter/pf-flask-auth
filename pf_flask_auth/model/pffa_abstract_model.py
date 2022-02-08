from sqlalchemy import Integer
from pf_flask_auth.common.pffa_password_util import PasswordUtil
from pf_flask_db.pf_app_database import app_db
from pf_flask_db.pf_app_model import AppModel, BaseModel


class OperatorAbstract(AppModel):
    __abstract__ = True
    firstName = app_db.Column("first_name", app_db.String(100))
    lastName = app_db.Column("last_name", app_db.String(100))
    name = app_db.Column("name", app_db.String(100))
    email = app_db.Column("email", app_db.String(100), unique=True, index=True)
    username = app_db.Column("username", app_db.String(100), unique=True, index=True)
    password_hash = app_db.Column("password_hash", app_db.String(150), nullable=False, index=True)
    isVerified = app_db.Column("is_verified", app_db.Boolean, default=True)
    isActive = app_db.Column("is_active", app_db.Boolean, default=True)
    token = app_db.Column("token", app_db.String(200))

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = PasswordUtil.get_password_hash(password)

    def verify_password(self, password) -> bool:
        return PasswordUtil.validate_password(password, self.password_hash)


class OperatorTokenAbstract(BaseModel):
    __abstract__ = True
    id = app_db.Column("id", app_db.BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    token = app_db.Column("token", app_db.String(350), nullable=False)
    name = app_db.Column("name", app_db.String(25))
    created = app_db.Column("created", app_db.DateTime, default=app_db.func.now())
    updated = app_db.Column("updated", app_db.DateTime, default=app_db.func.now(), onupdate=app_db.func.now())
    tokenOwnerId = app_db.Column("token_owner_id", app_db.BigInteger().with_variant(Integer, "sqlite"), nullable=False)
