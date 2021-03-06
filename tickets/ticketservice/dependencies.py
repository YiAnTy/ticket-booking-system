from nameko.extensions import DependencyProvider
import redis
from ticketservice import config
from ticketservice.exceptions import NotFound


REDIS_URI_KEY = 'REDIS_URI'


class StorageWrapper:
    """
    Product storage

    A very simple example of a custom Nameko dependency. Simplified
    implementation of products database based on Redis key value store.
    Handling the product ID increments or keeping sorted sets of product
    names for ordering the products is out of the scope of this example.

    """

    NotFound = NotFound

    def __init__(self, client):
        self.client = client

    def _format_key(self, ticket_id):
        return 'tickets:{}'.format(ticket_id)

    def _from_hash(self, document):
        return {
            'ticket_id': document[b'ticket_id'].decode('utf-8'),
            'title': document[b'title'].decode('utf-8'),
            'status': document[b'status'].decode('utf-8'),
        }

    def get(self, ticket_id):
        # product = self.client.hgetall(self._format_key(ticket_id))
        product = self.client.hgetall(ticket_id)
        print(product)
        if not product:
            raise NotFound('Ticket ID {} does not exist'.format(ticket_id))
        else:
            return self._from_hash(product)

    def list(self):
        keys = self.client.keys(('*'))
        for key in keys:
            yield self._from_hash(self.client.hgetall(key))

    def create(self, ticket):
        # key = self.client.keys(self._format_key(ticket['ticket_id']))
        # self.client.hmset(self.client.keys((ticket['ticket_id'])), ticket)
        self.client.hmset((ticket['ticket_id']), ticket)

    def decrement_stock(self, product_id, amount):
        return self.client.hincrby(
            self._format_key(product_id), 'in_stock', -amount)

    def change_status(self, ticket_id, status):
        product = self.client.hgetall(ticket_id)
        self.client.hmset(ticket_id, {'status': status})


class Storage(DependencyProvider):

    def setup(self):
         self.client = redis.StrictRedis.from_url('redis://user:test123@localhost:6379/10')
        # self.client = redis.StrictRedis.from_url('redis://@localhost:6379/11')
        #self.client = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, password='')

    def get_dependency(self, worker_ctx):
        return StorageWrapper(self.client)


class RedisClient(object):
    """
    redis client
    """
    redis_client = {}

    @staticmethod
    def reload_redis(host, port, select_db):
        """
        function: reload redis object
        """
        return redis.StrictRedis(
            host=host,
            port=port,
            db=select_db,
            password="",
            decode_responses=True)

    @classmethod
    def get_redis(cls, redis_name, host, port, select_db):
        """
        function: get redis client
        """
        if redis_name not in cls.redis_client:
            cls.redis_client[redis_name] = cls.reload_redis(
                host, port, select_db)
        return cls.redis_client.get(redis_name)
