from marshmallow import Schema, fields

class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    parent_id = fields.Int(allow_none=True)
    children = fields.Nested(lambda: CategorySchema(), many=True, dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    promo_price = fields.Float(allow_none=True)
    stock = fields.Int()
    desc = fields.Str()
    image_url = fields.Str()
    is_active = fields.Boolean()
    category_id = fields.Int(allow_none=True)
    category = fields.Nested(CategorySchema, dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
