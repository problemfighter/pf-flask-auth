from flask import Flask
from pf_flask_db.pf_app_model import AppModel
from pf_flask_db.pf_app_database import app_db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pf-flask-auth-quick-start.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app_db.init_app(app)


class Xyz:
    abc = app_db.Column(app_db.String(150), nullable=False)


abc = Xyz


class Person(AppModel, abc):
    first_name = app_db.Column(app_db.String(150), nullable=False)
    last_name = app_db.Column(app_db.String(150))
    email = app_db.Column(app_db.String(120), nullable=False)
    age = app_db.Column(app_db.Integer)
    income = app_db.Column(app_db.Float, default=0)


with app.app_context():
    app_db.create_all()


@app.route('/')
def bismillah():
    return "PF Flask Auth Tutorial"


if __name__ == '__main__':
    app.run(debug=True)
