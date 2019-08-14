import src.db_hdl as DB
import datetime


def add_order(phone_number):
    max_id = DB.query_db("select max(order_id) from orders")[0]['max(order_id)']
    if max_id is None:
        max_id = 1
    receiver_id = DB.query_db("select receiver_detail from user where phone_number=?", (phone_number,))[0][
        'receiver_detail']
    receiver_detail = DB.query_db("select * from receiver_detail where id=?", (receiver_id,))[0]

    cart_records = DB.query_db("select * from cart_records where phone_number=?", (phone_number,))
    for record in cart_records:
        DB.query_db(
            "insert into orders(order_id, phone_number, item, item_price_type, quantity, receiver_name, receiver_address, receiver_phone, order_time) values (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (max_id + 1, phone_number, record['item'], record['item_price_type'], record['quantity'],
            receiver_detail['receiver_name'], receiver_detail['receiver_address'], receiver_detail['receiver_phone'], datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))


def get_orders():
    result = []
    orders = DB.query_db("select * from orders")
    for order in orders:
        item_name = DB.query_db("select name from item where id=?", (order['item'],))
        _order = {}
        for row in order:
            _order[row] = order[row]
        item_id = _order['item']
        _order['item'] = item_name[0]['name']
        _order['price'] = int(_order['quantity']) * int(DB.query_db("select price from item_price where item=? and price_type=?", (item_id, _order["item_price_type"])))
        result += [_order]
    return result


def get_order_by_phone(phone_number):
    result = []
    orders = DB.query_db("select * from orders where phone_number=?", (phone_number,))
    for order in orders:
        item_name = DB.query_db("select name from item where id=?", (order['item'],))
        _order = {}
        for row in order:
            _order[row] = order[row]
        item_id = _order['item']

        _order['item'] = item_name[0]['name']
        _order['price'] = int(_order['quantity']) * int(DB.query_db("select price from item_price where item=? and price_type=?", (item_id, _order["item_price_type"])))
        result += [_order]
    return result
