from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3))
    email = fields.Email(required=True)
    full_name = fields.Str()
    is_admin = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

class RegisterSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3))
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
    full_name = fields.Str()
