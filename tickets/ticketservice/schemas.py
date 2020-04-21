from marshmallow import Schema, fields


class Ticket(Schema):
    id = fields.Str(required=True)
    title = fields.Str(required=True)
