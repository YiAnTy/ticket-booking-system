from nameko.rpc import rpc


class UserService(object):
    name = "userService"

    # add user account function
    @rpc
    def add_account(self):
        return None

    # delete user account function
    @rpc
    def delete_account(self):
        return None