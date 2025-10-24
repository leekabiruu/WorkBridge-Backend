from marshmallow import Schema, fields

class JobSchema(Schema):
    id = fields.Int(dump_only=True)
    employer_id = fields.Int(required=True)
    title = fields.Str(required=True)
    description = fields.Str()
    location = fields.Str()
    job_type = fields.Str()
    salary_range = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
