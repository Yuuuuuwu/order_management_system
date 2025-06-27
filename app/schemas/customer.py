from marshmallow import Schema, fields

class CustomerSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    phone = fields.Str()
    address = fields.Str()
    email = fields.Str()
    tags = fields.List(fields.Str())
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
