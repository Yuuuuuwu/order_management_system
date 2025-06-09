# app/schemas.py

from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.String(
        required=True,
        validate=validate.Length(min=3, max=64)
    )
    email = fields.Email(
        required=True,
        error_messages={
            "required": "需要 email (email is required)",
            "invalid": "email 格式不正確 (Invalid email format)"
        }
    )
    role = fields.String(validate=validate.OneOf(["buyer", "seller", "admin"]))
    is_active = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    last_login = fields.DateTime(dump_only=True)

class StoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    owner_id = fields.Int(required=True)
    contact = fields.String()
    address = fields.String()
    is_active = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    price = fields.Float(required=True)
    stock = fields.Int()
    desc = fields.String()
    image_url = fields.String()
    is_active = fields.Boolean()
    store_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class OrderItemSchema(Schema):
    id = fields.Int(dump_only=True)
    order_id = fields.Int(required=True)
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True)
    unit_price = fields.Float(required=True)
    total_price = fields.Float(required=True)
    created_at = fields.DateTime(dump_only=True)

class OrderSchema(Schema):
    id = fields.Int(dump_only=True)
    order_sn = fields.String(required=True)
    user_id = fields.Int(required=True)
    total_amount = fields.Float(required=True)
    status = fields.String()
    shipping_fee = fields.Float()
    payment_status = fields.String()
    remark = fields.String()
    receiver_name = fields.String(required=True)
    receiver_phone = fields.String(required=True)
    shipping_address = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    order_items = fields.Nested(OrderItemSchema, many=True, dump_only=True)

class PaymentSchema(Schema):
    id = fields.Int(dump_only=True)
    order_id = fields.Int(required=True)
    amount = fields.Float(required=True)
    status = fields.String()
    payment_method = fields.String(required=True)
    transaction_id = fields.String()
    paid_at = fields.DateTime()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

# 單筆與多筆序列化
user_schema = UserSchema()
users_schema = UserSchema(many=True)
store_schema = StoreSchema()
stores_schema = StoreSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
order_item_schema = OrderItemSchema()
order_items_schema = OrderItemSchema(many=True)
payment_schema = PaymentSchema()
payments_schema = PaymentSchema(many=True)