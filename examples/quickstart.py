from flask import Flask, redirect

from pf_flask_auth.common.pffa_auth_config import PFFAuthConfig
from pf_flask_auth.model.operator_token import app_db as operator_token
from pf_flask_auth.model.operator import app_db as operator
from pf_flask_auth.pf_flask_auth import pf_flask_auth
from pf_flask_db.pf_app_database import app_db
from pf_flask_mail.common.pffm_config import PFFMConfig

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pf-flask-auth-quick-start.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'SecretKey'

pf_flask_auth.init_app(app)

PFFAuthConfig.emailFormAppBaseURL = "http://127.0.0.1:5000"
config = PFFMConfig()
config.smtpServer = "smtp.gmail.com"
config.smtpUser = "pfdevtester@gmail.com"
config.smtpPassword = ""
config.smtpPort = 465
PFFAuthConfig.emailConfig = config


app_db.init_app(app)
with app.app_context():
    operator.create_all()
    operator_token.create_all()


@app.route('/')
def bismillah():
    return redirect("/auth")


if __name__ == '__main__':
    app.run(debug=True)
