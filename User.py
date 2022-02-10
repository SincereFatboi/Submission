class User:

    def __init__(self, email, password, password_confirm):
        self.__email = email
        self.__password = password
        self.__password_confirm = password_confirm

    def get_email(self):
        return self.__email

    def set_email(self, email):
        self.__email = email

    def get_password(self):
        return self.__password

    def set_cofirm_password(self, password):
        self.__password = password

    def get_password_confirm(self):
        return self.__password_confirm

    def set_password_confirm(self, password_confirm):
        self.__password_confirm = password_confirm

