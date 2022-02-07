from pf_flask_auth.common.pffa_auth_config import PFFAuthConfig
from pf_flask_auth.common.pffa_password_util import PasswordUtil
from pf_flask_db.pf_app_database import app_db
from pf_flask_db.pf_app_model import AppModel


class Operator(AppModel, PFFAuthConfig.operatorExtend):
    __abstract__ = not PFFAuthConfig.isCreateDefaultModel
    firstName = app_db.Column("first_name", app_db.String(100))
    lastName = app_db.Column("last_name", app_db.String(100))
    name = app_db.Column("name", app_db.String(100))
    email = app_db.Column("email", app_db.String(100), unique=True, index=True)
    username = app_db.Column("username", app_db.String(100), unique=True, index=True)
    password_hash = app_db.Column("password_hash", app_db.String(150), nullable=False, index=True)
    isVerified = app_db.Column("is_verified", app_db.Boolean, default=True)
    isActive = app_db.Column("is_active", app_db.Boolean, default=True)
    token = app_db.Column("token", app_db.String(200))
    tokens = app_db.relationship('OperatorToken', backref='operator', lazy=True)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = PasswordUtil.get_password_hash(password)

    def verify_password(self, password) -> bool:
        return PasswordUtil.validate_password(password, self.password_hash)
