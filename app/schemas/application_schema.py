from marshmallow import Schema, fields

class ApplicationSchema(Schema):
    id = fields.Int(dump_only=True)
    job_id = fields.Int(required=True)
    jobseeker_id = fields.Int(required=True)
    cover_letter = fields.Str()
    status = fields.Str()
    created_at = fields.DateTime(dump_only=True)
