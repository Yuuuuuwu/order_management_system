from marshmallow import Schema, fields

class ProductForm(Schema):
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    stock = fields.Int()
    desc = fields.Str()
    image_url = fields.Str()
