from marshmallow import Schema, fields

class FavoriteSchema(Schema):
    id = fields.Int(dump_only=True)
    job_id = fields.Int(required=True)
    jobseeker_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
