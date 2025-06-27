from marshmallow import Schema, fields

class ProductForm(Schema):
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    promo_price = fields.Float(allow_none=True)
    stock = fields.Int()
    desc = fields.Str()
    image_url = fields.Str()
    is_active = fields.Boolean()
    category_id = fields.Int(allow_none=True)

class CategoryForm(Schema):
    name = fields.Str(required=True)
    parent_id = fields.Int(allow_none=True)
