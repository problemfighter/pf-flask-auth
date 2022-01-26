from flask import Flask, redirect
from pf_flask_auth.model.operator_token import app_db as operator_token
from pf_flask_auth.model.operator import app_db as operator
from pf_flask_auth.pf_flask_auth import pf_flask_auth
from pf_flask_db.pf_app_database import app_db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pf-flask-auth-quick-start.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

pf_flask_auth.init_app(app)


app_db.init_app(app)
with app.app_context():
    operator.create_all()
    operator_token.create_all()


@app.route('/')
def bismillah():
    return redirect("/auth")


if __name__ == '__main__':
    app.run(debug=True)
