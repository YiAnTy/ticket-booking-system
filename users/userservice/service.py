from nameko.rpc import rpc

from userservice.models import Session, Account
from userservice import schemas
from userservice.exceptions import NotFound


class UsersService:
    name = "userService"

    db = Session()

    @rpc
    def add_account(self, account):
        account = Account(user_name=account['user_name'])

        self.db.add(account)
        self.db.commit()

        account = schemas.AccountSchema().dump(account)

        return account

    @rpc
    def get_account(self, user_name):
        account = self.db.query(Account).get(user_name)
        if not account:
            raise NotFound('User with name {} not found'.format(user_name))

        return schemas.AccountSchema().dump(account)