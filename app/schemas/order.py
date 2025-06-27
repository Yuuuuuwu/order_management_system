from marshmallow import Schema, fields

class OrderItemSchema(Schema):
    id = fields.Int(dump_only=True)
    order_id = fields.Int()
    product_id = fields.Int()
    product_name = fields.Str()
    qty = fields.Int()
    price = fields.Float()
    created_at = fields.DateTime(dump_only=True)

class OrderHistorySchema(Schema):
    id = fields.Int(dump_only=True)
    order_id = fields.Int()
    status = fields.Str()
    operator = fields.Str()
    operated_at = fields.DateTime()
    remark = fields.Str()

class OrderSchema(Schema):
    id = fields.Int(dump_only=True)
    order_sn = fields.Str(required=True)
    user_id = fields.Int(required=True)
    total_amount = fields.Float(required=True)
    status = fields.Str()
    shipping_fee = fields.Float()
    payment_status = fields.Str()
    remark = fields.Str()
    receiver_name = fields.Str(required=True)
    receiver_phone = fields.Str(required=True)
    shipping_address = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    items = fields.Nested(OrderItemSchema, many=True, dump_only=True)
    history = fields.Nested(OrderHistorySchema, many=True, dump_only=True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
