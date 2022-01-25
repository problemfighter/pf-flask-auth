from flask import Flask

from pf_flask_auth.pf_flask_auth import pf_flask_auth

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pf-flask-auth-quick-start.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

pf_flask_auth.init_app(app)


@app.route('/')
def bismillah():
    return "PF Flask Auth Tutorial"


if __name__ == '__main__':
    app.run(debug=True)
