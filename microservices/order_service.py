from nameko.rpc import rpc

class OrderService(object):
    name = "orderService"

    # cancel order api
    @rpc
    def cancel_order(self):
        return None

    # place order api
    @rpc
    def palce_order(self):
        return None