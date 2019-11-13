from flask_login import UserMixin
from src.db_hdl import *

class User(UserMixin):

    def __init__(self, form):
        if form is not None:
            self.phone_number = form["phone_number"]
            self.verification_code = form["verification_code"]
            self.password = form["password"]
            self.nick_name = form["nick_name"]

    def get_id(self):
        return self.phone_number

def get_user(phone_number):
    return User(query_db("""
                SELECT * FROM user WHERE phone_number="%s";
            """ % (phone_number), (), one=True))

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
