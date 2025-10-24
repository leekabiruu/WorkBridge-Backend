from marshmallow import Schema, fields

class MessageSchema(Schema):
    id = fields.Int(dump_only=True)
    sender_id = fields.Int(required=True)
    recipient_id = fields.Int(required=True)
    text = fields.Str(required=True)
    attachment_url = fields.Str()
    timestamp = fields.DateTime(dump_only=True)
