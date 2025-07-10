from marshmallow import Schema, fields, validate

class UserRegisterForm(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=2))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    role = fields.Str(validate=validate.OneOf(["admin", "seller", "customer"]))

class UserLoginForm(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
