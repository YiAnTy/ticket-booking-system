from nameko.events import EventDispatcher
from nameko.rpc import rpc

from orderservice.exceptions import NotFound
from orderservice.models import Session, Order, OrderDetail
from orderservice.schemas import OrderSchema


class OrdersService:
    name = 'orderService'

    db = Session()
    event_dispatcher = EventDispatcher()

    @rpc
    def get_order(self, order_id):
        order = self.db.query(Order).get(order_id)

        if not order:
            raise NotFound('Order with id {} not found'.format(order_id))

        return OrderSchema().dump(order)

    @rpc
    def create_order(self, order_details):
        order = Order(
            order_details=[
                OrderDetail(
                    ticket_id=order_detail['ticket_id'],
                    price=order_detail['price']
                )
                for order_detail in order_details
            ]
        )
        self.db.add(order)
        self.db.commit()

        order = OrderSchema().dump(order)

        self.event_dispatcher('order_created', {
            'order': order,
        })

        return order

    @rpc
    def update_order(self, order):
        order_details = {
            order_details['id']: order_details
            for order_details in order['order_details']
        }

        order = self.db.query(Order).get(order['id'])

        for order_detail in order.order_details:
            order_detail.price = order_details[order_detail.id]['price']
            order_detail.quantity = order_details[order_detail.id]['quantity']

        self.db.commit()
        return OrderSchema().dump(order)

    @rpc
    def delete_order(self, order_id):
        order = self.db.query(Order).get(order_id)
        self.db.delete(order)
        self.db.commit()
