from src.db_hdl import *
from src.item import *


class cart_record:

    def __init__(self,item_id,item_price_type,quantity):
        item = get_item_by_id(item_id)
        self.item_id = item_id
        self.item_name = item.name
        self.item_price_type = item_price_type
        self.quantity = quantity

        for priceType in item.price_list:
            if priceType["price_type"] == item_price_type:
                self.price = priceType["price"]



def get_records(phone_number):
    records = query_db("select item,item_price_type,quantity from cart_records where phone_number = ?;",(phone_number,))
    records_list = []
    for record in records:
        records_list.append(cart_record(record["item"], record["item_price_type"],record["quantity"]).__dict__)
    return records_list

def add_record(phone_number, item_id, item_price_type, quantity):
    query_db("INSERT INTO cart_records(phone_number, item, item_price_type, quantity) VALUES (?,?,?,?);",(phone_number,item_id,item_price_type,quantity))
    return

def updata_quantity(phone_number, item_id, item_price_type, quantity):
    execute_db("UPDATE cart_records SET quantity=? WHERE phone_number=? and item=? and item_price_type=?;",(quantity,phone_number,item_id,item_price_type))
    return


def delete_item(phone_number, item_id, item_price_type):
    execute_db("DELETE FROM cart_records WHERE phone_number=? and item=? and item_price_type=?;",
               (phone_number, item_id, item_price_type))
    return


def get_cart(phone_number):
    records = execute_db("SELECT * FROM cart_records WHERE phone_number=?;",
               phone_number)
    return


def clear(phone_number):
    execute_db("DELETE FROM cart_records WHERE phone_number=?;",
               (phone_number,))
