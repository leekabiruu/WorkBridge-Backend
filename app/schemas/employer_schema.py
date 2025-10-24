from marshmallow import Schema, fields

class EmployerSchema(Schema): 
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    company_name = fields.Str(required=True)
    company_description = fields.Str()
    website = fields.Str()
    logo_url = fields.Str()
    phone = fields.Str()
    location = fields.Str()
