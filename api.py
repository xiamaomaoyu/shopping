from flask import jsonify, Blueprint, request, abort, make_response
import src.search as search
import src.item as item
from src.db_hdl import *
import src.receiver_detail as ReceiverDetail
import src.order as Order
from src.sms_hdl import send_customer
import src.cart_hdl as Cart
from src.user import *
import random


api = Blueprint('api',__name__)


@api.route('/api/search/all_items',methods=['POST', 'GET'])
def all_items():
    return jsonify(search.all_item())


@api.route('/api/search/all_item_names',methods=['POST', 'GET'])
def all_item_name():
    return jsonify(search.all_item_name())


@api.route('/api/search/keyword/',methods=['POST', 'GET'])
@api.route('/api/search/keyword/<keyword>',methods=['POST', 'GET'])
def items_by_keyword(keyword=None):
    if keyword:
        return jsonify(search.items_by_keyword(keyword))
    else:
        return all_items()


@api.route('/api/item/<id>',methods=['POST', 'GET'])
def item_by_id(id):
    return jsonify(item.get_item_by_id(id).json())


@api.route('/api/login/send_verification_code/<phone_number>', methods=['POST','GET'])
def send_verification_code(phone_number):
    user = query_db("""
                    SELECT * FROM user WHERE phone_number="%s";
                """ % (phone_number), ())
    if len(user) == 0:
        add_user(phone_number,"123","NEWUSER")

    new_verification_code = str(random.randint(100000, 999999))
    execute_db("""
        UPDATE user SET verification_code=? WHERE phone_number = ?;
    """, (new_verification_code,phone_number))
    message = "welcome, your verification code is：" + new_verification_code
    send_customer(phone_number=phone_number, text=message)
    return make_response(jsonify(message='success'), 200)


@api.route('/api/login/update_info', methods=['POST','GET'])
def login_update_info():
    phone_number = request.form.get("phone_number")
    nickname = request.form.get("nickname")
    password = request.form.get("password")
    update_nickname(phone_number,nickname)
    update_password(phone_number,password)

    return make_response(jsonify(message='success'), 200)


@api.route('/api/cart/get_records/<phone_number>', methods=['POST','GET'])
def get_records(phone_number):
    print(Cart.get_records(phone_number))
    return jsonify(Cart.get_records(phone_number))


@api.route('/api/cart/add_record', methods=['POST','GET'])
def add_record():
    phone_number = request.form.get("phone_number")
    item_id = request.form.get("item_id")
    item_price_type = request.form.get("item_price_type")
    quantity = request.form.get("quantity")
    Cart.add_record(phone_number,item_id,item_price_type,quantity)
    return make_response(jsonify(message='success'), 200)


@api.route('/api/cart/update_quantity',methods=['POST','GET'])
def update_quantity():
    phone_number = request.form.get("phone_number")
    item_id = request.form.get("item_id")
    item_price_type = request.form.get("item_price_type")
    quantity = request.form.get("quantity")
    Cart.updata_quantity(phone_number,item_id,item_price_type,quantity)
    return make_response(jsonify(message='success'), 200)


@api.route('/api/cart/delete_item/<item_id>/<phone_number>/<item_price_type>',methods=['POST','GET'])
def delete_item(item_id, phone_number, item_price_type):
    Cart.delete_item(phone_number,item_id,item_price_type)
    return make_response(jsonify(message='success'), 200)


@api.route('/api/receiver_detail/get_details/<phone_number>',methods=['POST','GET'])
def get_details(phone_number):
    details = ReceiverDetail.get_receiver_details(phone_number)
    return make_response(jsonify(message='success', details=details), 200)


@api.route('/api/receiver_detail/delete_detail/<detail_id>',methods=['POST','GET'])
def delete_details(detail_id):
    ReceiverDetail.delete_detail(detail_id)
    return make_response(jsonify(message='success'), 200)


@api.route('/api/receiver_detail/add_detail/<phone_number>/<receiver_name>/<receiver_address>/<receiver_phone>',methods=['POST','GET'])
def add_detail(phone_number, receiver_name, receiver_address, receiver_phone):
    ReceiverDetail.add_receiver_details(phone_number, receiver_name,receiver_address,receiver_phone)
    return make_response(jsonify(message='success'), 200)


@api.route('/api/receiver_detail/set_detail/<phone_number>/<detail_id>',methods=['POST','GET'])
def set_detail(phone_number, detail_id):
    ReceiverDetail.set_as_receiver(phone_number, detail_id)
    return make_response(jsonify(message='success'), 200)


@api.route('/api/save_order/<phone_number>',methods=['POST','GET'])
def save_order(phone_number):
    """
    When we save the order we should calculate the overall price.
    After save the order, then we can get the overall price thought orders and status
    :param phone_number: the user phone number
    :return:
    """
    order_id = Order.add_order(phone_number)
    Cart.clear(phone_number)
    return make_response(jsonify(message='success', order_id=order_id), 200)


@api.route('/api/get_orders',methods=['POST','GET'])
def get_orders():
    return make_response(jsonify(message='success', orders=Order.get_orders()), 200)


@api.route('/api/get_order/<phone_number>',methods=['POST','GET'])
def get_order_by_phone(phone_number):
    return make_response(jsonify(message='success', orders=Order.get_order_by_phone(phone_number)), 200)


@api.route('/api/get_order/<phone_number>/<status>',methods=['POST','GET'])
def get_order_by_phone_status(phone_number, status):
    return make_response(jsonify(message='success', orders=Order.get_order_by_phone_status(phone_number, status)), 200)


@api.route('/api/set_order_status/<order_id>/<status>',methods=['POST','GET'])
def set_order_status(order_id, status):
    return make_response(jsonify(message='success', orders=Order.set_order_status(order_id, status)), 200)


@api.route('/api/get_order_comment/<order_id>',methods=['POST','GET'])
def get_order_comment(order_id, status):
    return make_response(jsonify(message='success', orders=Order.get_order_comment(order_id)), 200)


@api.route('/api/set_order_comment/<order_id>',methods=['POST','GET'])
def set_order_comment(order_id):
    comment = request.args.get("comment")
    rating = request.args.get("rating")

    return make_response(jsonify(message='success', orders=Order.set_order_comment(order_id, comment, rating)), 200)


@api.route('/api/get_all_orders',methods=['POST','GET'])
def get_all_orders():
    return make_response(jsonify(message='success', orders=Order.get_all_orders()), 200)


@api.route('/api/add_pay_no/<pay_id>/<order_id>', methods=['POST','GET'])
def set_pay_no(pay_id, order_id):
    """
    store the payment order id into orders table according to order id
    :param pay_id: the payment id from omipay
    :param order_id: the order of user is paying
    :return:
    """
    Order.add_pay_order_no(order_id, pay_id)
    return make_response(jsonify(message="success"), 200)


@api.route('/api/get_overall_price/<order_id>', methods=['POST','GET'])
def overall_price(order_id):
    """
    get the overall price of this order id
    :param order_id: the order with need to pay
    :return:
    """
    op = Order.get_overall_price(order_id)
    return make_response(jsonify(overall_price=op), 200)


@api.route('/api/pay_status/<order_id>', methods=['POST','GET'])
def pay_status(order_id):
    """
    check whether pay success,
        if success then sent
        else do nothing
    :param order_id: the payed order id
    :return:
    """
    Order.check_pay(order_id)


@api.route('/api/delivery_history/<order_id>', methods=['POST','GET'])
def delivery_history(order_id):
    """
    get the delivery history according to order id
    :param order_id:
    :return:
    """
    history = Order.check_delivery_id(order_id)
    # if can not get the history then abort error
    if history is None:
        return make_response(jsonify(message='error'), 400)

    return make_response(jsonify({"res": history}), 200)
