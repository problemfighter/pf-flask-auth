import click
from flask.cli import AppGroup, with_appcontext

from pf_flask_auth.service.operator_cli_service import operator_cli_service

pf_flask_auth_cli = AppGroup("auth-cli", help="PF Flask Auth Manipulation")


@pf_flask_auth_cli.command("create", help="Create Operator")
@click.option("--email", prompt="Enter Email ", help="Provide your email address", required=True)
@click.option("--password", prompt="Enter Password ", help="Provide your password", hide_input=True, required=True)
@with_appcontext
def create(email, password):
    response = operator_cli_service.create_operator_by_email({"email": email, "password": password})
    print(response)


# @pf_flask_auth_cli.command("destroy", help="Delete database tables")
# @with_appcontext
# def destroy():
#     pass
