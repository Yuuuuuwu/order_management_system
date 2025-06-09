from marshmallow import Schema, fields

class PaymentSchema(Schema):
    id = fields.Int(dump_only=True)
    order_id = fields.Int(required=True)
    amount = fields.Float(required=True)
    status = fields.Str()
    payment_method = fields.Str(required=True)
    transaction_id = fields.Str()
    paid_at = fields.DateTime()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
