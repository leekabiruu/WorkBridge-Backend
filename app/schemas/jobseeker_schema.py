from marshmallow import Schema, fields

class JobSeekerSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    bio = fields.Str()
    resume_url = fields.Str()
    skills = fields.Str()
    experience = fields.Str()
    education = fields.Str()
    location = fields.Str()
