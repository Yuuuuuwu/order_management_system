from marshmallow import Schema, fields

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
