from nameko.events import EventDispatcher, event_handler
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
    def create_order(self, order_details, account_id, status):
        order = Order(
            order_details=[
                OrderDetail(
                    ticket_id=order_detail['ticket_id'],
                    price=order_detail['price']
                )
                for order_detail in order_details
            ],
            account_id=account_id,
            status=status
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
        status = order['status']
        order = self.db.query(Order).get(order['id'])
        order.status = status
        for order_detail in order.order_details:
            order_detail.price = order_details[order_detail.id]['price']

        self.db.commit()
        return OrderSchema().dump(order)

    @rpc
    def delete_order(self, order_id):
        order = self.db.query(Order).get(order_id)
        self.db.delete(order)
        self.db.commit()

    @event_handler('paymentService', 'pay_success')
    def handle_payment(self, payment):
        print(payment['payment']['status'])
        if payment['payment']['status'] == 1:
            order = self.get_order(payment['payment']['order_id'])
            order = OrderSchema().dump(order)
            order['status'] = 1
            print(order)
            self.update_order(order)
            self.event_dispatcher('order_success',{'order': order})

    @event_handler('paymentService', 'refund')
    def handle_refund(self, payment):
        if payment['payment']['status'] == 2:
            order = self.get_order(payment['payment']['order_id'])
            order = OrderSchema().dump(order)
            order['status'] = 2
            print(order)
            self.update_order(order)
            self.event_dispatcher('order_cancel', {'order': order})