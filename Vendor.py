from User import User
import uuid


class Vendor(User):

    def __init__(self, name, username, mobile, email, password, password_confirm):
        super().__init__(email, password, password_confirm)
        self.__class__.count_id = str(uuid.uuid4())
        self.__vendor_id = self.__class__.count_id
        self.__username = username
        self.__name = name
        self.__mobile = mobile

    def get_vendor_id(self):
        return self.__vendor_id

    def set_vendor_id(self, vendor_id):
        self.__vendor_id = vendor_id

    def get_username(self):
        return self.__username

    def set_username(self, username):
        self.__username = username

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_mobile(self):
        return self.__mobile

    def set_mobile(self, mobile):
        self.__mobile = mobile

