from marshmallow import Schema, fields


class CreateOrderDetailSchema(Schema):
    ticket_id = fields.Str(required=True)
    price = fields.Decimal(as_string=True, required=True)


class CreateOrderSchema(Schema):
    order_details = fields.Nested(
        CreateOrderDetailSchema, many=True, required=True
    )


class TicketSchema(Schema):
    ticket_id = fields.Str(required=True)
    title = fields.Str(required=True)
    placed = fields.Str(required=True)


class GetOrderSchema(Schema):

    class OrderDetail(Schema):
        id = fields.Int()
        ticket_id = fields.Str()
        price = fields.Decimal(as_string=True)
        ticket = fields.Nested(TicketSchema, many=False)

    id = fields.Int()
    order_details = fields.Nested(OrderDetail, many=True)
