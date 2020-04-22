from nameko.rpc import rpc
from nameko.events import EventDispatcher
from paymentservice import schemas
from paymentservice.models import Session, Payment

import datetime


class PaymentService:
    name = "paymentService"
    db = Session()

    event_dispatcher = EventDispatcher()

    @rpc
    def pay(self, order, status):
        total_price = 0
        for orderdetail in order['order_details']:
            total_price += float(orderdetail['price'])

        payment = Payment(order_id=order['id'],total_price=total_price,status=status)
        self.db.add(payment)
        self.db.commit()
        payment = schemas.PaymentSchema().dump(payment)

        self.event_dispatcher('payment', {'payment': payment})
        return payment

    @rpc
    def refund(self, order_id):
        payment = self.db.query(Payment).filter(Payment.order_id == order_id).first()
        print(payment)
        payment.status = 2
        self.db.commit()

        payment = schemas.PaymentSchema().dump(payment)

        self.event_dispatcher('refund', {'payment': payment})
        return payment
