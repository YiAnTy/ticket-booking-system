from marshmallow import Schema, fields


class AccountSchema(Schema):
    account_id = fields.Int(required=True)
    user_name = fields.Str(required=True)
