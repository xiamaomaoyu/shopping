from flask_login import UserMixin
from src.db_hdl import *


class User(UserMixin):

    def __init__(self, form):
        if isinstance(form, dict):
            self.phone_number = form["phone_number"]
            self.verification_code = form["verification_code"]
            self.password = form["password"]
            self.nick_name = form["nick_name"]

    def get_id(self):
        return self.phone_number

    def get_type(self):
        return "User"


class Admin(UserMixin):

    def __init__(self, admin_name):
        self.admin_name = admin_name

    def get_id(self):
        return self.admin_name

    def get_type(self):
        return "Admin"


def get_admin(admin_name):
    return Admin(admin_name)

def get_user(phone_number):
    row = query_db("""
                SELECT * FROM user WHERE phone_number="%s";
            """ % (phone_number), (), one=True)
    if row is None:
        return Admin(phone_number)
    else:
        return User(row)

def add_user(phone_number, password, nick_name):
    execute_db("""
            INSERT INTO user(phone_number,verification_code, password, nick_name) VALUES (?, ?,?,?);

        """ , (phone_number,"000000",password,nick_name))

def update_nickname(phone_number,nickname):
    execute_db("""
        UPDATE user set nick_name=? where phone_number=?;
    """,(nickname,phone_number))

def update_password(phone_number,password):
    execute_db("""
        UPDATE user set password=? where phone_number=?;
    """,(password,phone_number))
