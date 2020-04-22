from marshmallow import Schema, fields


class Ticket(Schema):
    ticket_id = fields.Str(required=True)
    title = fields.Str(required=True)
    placed = fields.Str(required=True)
