from nameko.rpc import rpc


class PaymentService(object):
    name = "paymentService"

    # pay bill api
    @rpc
    def pay(self):
        return None



