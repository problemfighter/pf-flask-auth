from marshmallow import fields
from pf_flask_rest.form.pf_app_form_def import FormAppDef


class OperatorDTO(FormAppDef):
    firstName = fields.String()
    lastName = fields.String()
    name = fields.String()
    email = fields.Email()
    username = fields.String()
    profilePhoto = fields.String()
    coverPhoto = fields.String()
