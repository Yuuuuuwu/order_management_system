from marshmallow import Schema, fields

class OrderForm(Schema):
    order_sn = fields.Str(required=True)
    user_id = fields.Int(required=True)
    total_amount = fields.Float(required=True)
    receiver_name = fields.Str(required=True)
    receiver_phone = fields.Str(required=True)
    shipping_address = fields.Str(required=True)
