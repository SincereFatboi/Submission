from User import User
import uuid


class Customer(User):

    def __init__(self, username, email, password, password_confirm):
        super().__init__(email, password, password_confirm)
        self.__class__.count_id = "C" + str(uuid.uuid4())
        self.__customer_id = self.__class__.count_id
        self.__username = username

    def get_customer_id(self):
        return self.__customer_id

    def set_customer_id(self, customer_id):
        self.__customer_id = customer_id

    def get_username(self):
        return self.__username

    def set_username(self, username):
        self.__username = username


