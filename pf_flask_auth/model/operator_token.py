from sqlalchemy import Integer
from pf_flask_db.pf_app_database import app_db
from pf_flask_db.pf_app_model import BaseModel


class OperatorToken(BaseModel):
    id = app_db.Column("id", app_db.BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    token = app_db.Column("token", app_db.String(350), nullable=False)
    name = app_db.Column("name", app_db.String(25))
    created = app_db.Column("created", app_db.DateTime, default=app_db.func.now())
    updated = app_db.Column("updated", app_db.DateTime, default=app_db.func.now(), onupdate=app_db.func.now())
    operatorId = app_db.Column("operator_id", app_db.BigInteger().with_variant(Integer, "sqlite"), app_db.ForeignKey('operator.id'), nullable=False)
