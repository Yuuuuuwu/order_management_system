from marshmallow import Schema, fields

class PaymentForm(Schema):
    order_id = fields.Int(required=True)
    amount = fields.Float(required=True)
    payment_method = fields.Str(required=True)
