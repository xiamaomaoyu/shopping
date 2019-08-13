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
    return jsonify(Cart.get_records(phone_number))

@api.route('/api/cart/add_record',methods=['POST','GET'])
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
    print("update ",phone_number," ",item_price_type,"   ",quantity)
    return make_response(jsonify(message='success'), 200)


@api.route('/api/cart/delete_item',methods=['POST','GET'])
def delete_item():
    item_id = request.form.get("item_id")
    phone_number = request.form.get("phone_number")
    item_price_type = request.form.get("item_price_type")
    print("delete ",phone_number," ",item_price_type,)
    Cart.delete_item(phone_number,item_id,item_price_type)
    return make_response(jsonify(message='success'), 200)

@api.route('/api/receiver_detail/get_details/<phone_number>',methods=['POST','GET'])
def get_details(phone_number):
    details = ReceiverDetail.get_receiver_details(phone_number)
    return make_response(jsonify(message='success', details=details), 200)

@api.route('/api/receiver_detail/delete_detail/<detail_id>',methods=['POST','GET'])
def get_details(detail_id):
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
    Order.add_order(phone_number)
    return make_response(jsonify(message='success'), 200)

@api.route('/api/get_orders',methods=['POST','GET'])
def get_orders():
    return make_response(jsonify(message='success', orders=Order.get_orders()), 200)

