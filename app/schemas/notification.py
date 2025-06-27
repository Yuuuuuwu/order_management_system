from marshmallow import Schema, fields

class OperationLogSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    username = fields.Str()
    action = fields.Str()
    target_type = fields.Str()
    target_id = fields.Int(allow_none=True)
    content = fields.Str()
    created_at = fields.DateTime()

class NotificationSchema(Schema):
    id = fields.Int()
    user_id = fields.Int(allow_none=True)
    type = fields.Str()
    title = fields.Str()
    content = fields.Str()
    is_read = fields.Bool()
    created_at = fields.DateTime()
