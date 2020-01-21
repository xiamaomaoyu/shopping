from flask import jsonify, Blueprint, request, make_response
import src.search as search
import src.item as item
import src.receiver_detail as ReceiverDetail
import src.order as Order
from src.sms_hdl import send_customer
import src.cart_hdl as Cart
from src.user import *
import random
from utils.request_handling import *
import shutil


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
    if phone_number[0] == '0':
        phone_number = phone_number[1:]
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
    return make_response(jsonify(message='success'),200)


# @api.route('/api/delivery_history/<order_id>', methods=['POST','GET'])
# def delivery_history(order_id):
#     """
#     get the delivery history according to order id
#     :param order_id:
#     :return:
#     """
#     history = Order.check_delivery_id(order_id)
#     # if can not get the history then abort error
#     if history is None:
#         return make_response(jsonify(message='error'), 400)
#     return make_response(jsonify({"res": history}), 200)
#
#
# @api.route('/api/make_delivery/<order_id>', methods=['POST','GET'])
# def add_delivery(order_id):
#     """
#     admin make the delivery
#     :param order_id:
#     :return:
#     """
#     res = Order.make_delivery(order_id)
#
#     if res is False:
#         return make_response(jsonify(message='Already send'), 400)
#
#     return make_response(jsonify(message='success'), 200)


############################################## NEW API ###########################


status = {
    'sent': '已发货',
    'paid': '已付款',
    'unpaid': '待付款',
    'unsent': '待发货',
    'uncomment': '待评价',
    'closed': '交易结束'
}


def switch_word(word):
    return status[word]


# for check the token
def check_user(token):
    """
    according to token, get the user's details
    :param token: the token arg
    :return: the user's information from database
    """
    user = query_db("SELECT * FROM staff WHERE token = ?", (token, ))
    if len(user) == 0:
        return False
    return True


# 登陆
@api.route('/api/staff/login', methods=['POST','GET'])
def login():
    username = get_request_args('username')
    password = get_request_args('password')

    user = query_db("SELECT * FROM staff WHERE username = ? AND password = ?",
                    (username, password), one=True)

    if user is None:
        return make_response(jsonify(message='用户名或者密码不对'), 400)

    token = get_token()
    query_db("UPDATE staff SET token=? WHERE username=? AND password=?",
             (token, username, password))
    return make_response(jsonify(token=token), 200)


@api.route('/api/order/all', methods=['POST','GET'])
def all_order():
    """
    得到所有的订单
    :return:
    """
    token = get_header(request)
    if not check_user(token):
        return make_response(jsonify(message='请先登陆'), 400)

    orders = query_db("SELECT * FROM orders GROUP BY order_id")
    for o in orders:
        o['key'] = o['order_id']
        o['overall_price'] = Order.get_overall_price(o['order_id'])
        o['status'] = switch_word(o['status'])
    return make_response(jsonify(data=orders))


@api.route('/api/sub-order/all', methods=['POST','GET'])
def sub_order():
    """
    得到相信订单信息
    :return:
    """
    token = get_header(request)
    if not check_user(token):
        return make_response(jsonify(message='请先登陆'), 400)

    res = query_db("SELECT * FROM orders")
    for o in res:
        o['key'] = o['order_id']
        price = query_db("SELECT price FROM item_price WHERE item = ? AND price_type = ?",
                         (o['item'], o['item_price_type']))
        o['price'] = price[0]['price']
    return make_response(jsonify(data=res), 200)


@api.route('/api/check-delivery/<id>', methods=['POST','GET'])
def check_delivery(id):
    """
    物流查询
    :param id:
    :return:
    """
    token = get_header(request)
    if not check_user(token):
        return make_response(jsonify(message='请先登陆'), 400)

    res = Order.check_delivery_id(id)
    if res is None:
        return make_response(jsonify(res='Incorrect order ID'), 404)

    return make_response(jsonify(res=res), 200)


@api.route('/api/feedback', methods=['POST','GET'])
def feedback():
    token = get_header(request)
    if not check_user(token):
        return make_response(jsonify(message='请先登陆'), 400)

    fbs = query_db("SELECT * FROM feedbacks")
    for fb in fbs:
        user = query_db("SELECT * FROM orders WHERE order_id = ?", (fb['order_id'],))
        fb['username'] = user[0]['phone_number']

    return make_response(jsonify(res=fbs), 200)


@api.route('/api/change', methods=['POST', 'GET'])
def change():
    """
    修改用户的收货信息
    收人
    收货人电话
    收货地址等
    :return:
    """
    token = get_header(request)
    if not check_user(token):
        return make_response(jsonify(message='请先登陆'), 400)

    receiver = get_request_args('receiver_name')
    phone = get_request_args('receiver_phone')
    address = get_request_args('receiver_address')
    order_id = get_request_args('order_id')

    query_db("UPDATE orders SET receiver_name=?, receiver_phone=?, receiver_address=? WHERE order_id=?",
             (receiver, phone, address, order_id))

    return make_response(jsonify(message='修改成功'), 200)


@api.route('/api/delete', methods=['POST', 'GET'])
def delete():
    """
    删除订单信息
    :return:
    """
    token = get_header(request)
    if not check_user(token):
        return make_response(jsonify(message='请先登陆'), 400)

    order_id = get_request_args('order_id')
    query_db("DELETE FROM orders WHERE order_id = ?", (order_id, ))

    return make_response(jsonify(message='删除成功'), 200)


@api.route('/api/item/all', methods=['POST', 'GET'])
def all_item():
    """
    获取所有的商品
    :return:
    """
    token = get_header(request)
    if not check_user(token):
        return make_response(jsonify(message='请先登陆'), 400)

    items = query_db("SELECT * FROM item")
    return make_response(jsonify(data=items), 200)


@api.route('/api/item-type/all',  methods=['POST', 'GET'])
def sub_items():
    """
    每个商品对应的价格类型以及价格
    :return:
    """
    token = get_header(request)
    if not check_user(token):
        return make_response(jsonify(message='请先登陆'), 400)

    item_type = query_db("SELECT * FROM item_price")
    return make_response(jsonify(data=item_type), 200)


@api.route('/api/make-delivery/<order_id>', methods=['POST','GET'])
def send_delivery(order_id):
    """
    发货
    :param order_id:
    :return:
    """
    token = get_header(request)
    if not check_user(token):
        return make_response(jsonify(message='请先登陆'), 400)

    # 如果返回是delivery id则表示发货成功
    # 如果是None表示没有成功
    res = Order.make_delivery(order_id)
    if res is None:
        return make_response(jsonify(message='已经发货'), 400)

    return make_response(jsonify(message='success', res=res), 200)


@api.route('/api/delete-item', methods=['POST','GET'])
def delete_item_api():
    """
    删除商品(item)
    :return:
    """
    token = get_header(request)
    if not check_user(token):
        return make_response(jsonify(message='请先登陆'), 400)

    item_id = get_request_args('item_id')
    item = query_db("SELECT * FROM item WHERE id=?", (item_id,), one=True)
    item_name = item['name']

    query_db("DELETE FROM item WHERE id = ?", (item_id, ))
    query_db("DELETE FROM item_price WHERE item=?", (item_id, ))

    # 同时删除照片
    file_path = "static/img/itemImg/%s" % item_name
    if os.path.isdir(file_path):
        shutil.rmtree(file_path)

    file_path = "static/img/discriptions/%s" % item_name
    if os.path.isdir(file_path):
        shutil.rmtree(file_path)

    return make_response(jsonify(message='删除商品成功'), 200)


@api.route('/api/delete-item-type', methods=['POST','GET'])
def delete_item_type():
    """
    删除item type和price
    :return:
    """
    token = get_header(request)
    if not check_user(token):
        return make_response(jsonify(message='请先登陆'), 400)

    item_id = get_request_args('item_id')
    item_type = get_request_args('item_type')
    query_db("DELETE FROM item_price WHERE item = ? AND price_type = ?",
             (item_id, item_type))

    return make_response(jsonify(message='删除成功'))


@api.route('/api/change-item-type', methods=['POST', 'GET'])
def change_item_type():
    """
    修改item type的price
    :return:
    """
    token = get_header(request)
    if not check_user(token):
        return make_response(jsonify(message='请先登陆'), 400)

    item_id = get_request_args('item_id')
    item_type = get_request_args('item_type')
    item_price = get_request_args('item_price')

    query_db("UPDATE item_price SET price = ? WHERE item=? AND price_type=?",
             (item_price, item_id, item_type))

    return make_response(jsonify(message='修改成功'), 200)


# 检查是否符合类型
allows = {'png', 'jpg', 'jpeg'}


# check whether allow type
def check_allow(file_name):
    return '.' in file_name and \
            file_name.rsplit('.', 1)[1].lower() in allows


@api.route('/api/add-item', methods=['POST', 'GET'])
def add_item():
    """
    添加新的商品
    :return:
    """
    # token = get_header(request)
    # if not check_user(token):
    #     return make_response(jsonify(message='请先登陆'), 400)

    item_name = get_request_args('name')
    item_price = get_request_args('price')
    tags = get_request_args('tags')
    weight = get_request_args('weight')
    product_name = get_request_args('product_name')

    # one: 单罐包邮, three: 三罐包邮, six 六罐包邮
    one = get_request_args('one', required=False)
    three = get_request_args('three', required=False)
    six = get_request_args('six', required=False)
    main_img = get_request_file('main_img')
    detail_img = get_request_file('detail_img')

    items = query_db("SELECT * FROM item")
    item = items[len(items) - 1]
    id = int(item['id']) + 1

    query_db("INSERT INTO item(id, name, tags, weight, product_name) VALUES (?, ?,?,?,?)",
             (id, item_name, tags, weight, product_name))

    query_db("INSERT INTO item_price(item, price_type, price) VALUES (?,?,?)",
             (id, '单罐', item_price))

    if one != 'undefined':
        query_db("INSERT INTO item_price(item, price_type, price) VALUES (?,?,?)",
                 (id, '单罐包邮', one))

    if three != 'undefined':
        query_db("INSERT INTO item_price(item, price_type, price) VALUES (?,?,?)",
                 (id, '三罐包邮', three))

    if six != 'undefined':
        query_db("INSERT INTO item_price(item, price_type, price) VALUES (?,?,?)",
                 (id, '六罐包邮', six))

    for mg in main_img:
        if mg and check_allow(mg.filename):
            target = "static/img/itemImg/%s" % item_name
            if not os.path.isdir(target):
                os.mkdir(target)

            filepath = target + "/main.jpg"
            mg.save(filepath)

    for dg in detail_img:
        if dg and check_allow(dg.filename):
            target = "static/img/discriptions/%s" % item_name
            if not os.path.isdir(target):
                os.mkdir(target)

            filepath = target + "/%s" % dg.filename
            dg.save(filepath)

    return make_response(jsonify(message='上传成功'), 200)


@api.route('/api/get-main-img', methods=['POST', 'GET'])
def get_main_img():
    """
    获取main photo
    :return:
    """
    token = get_header(request)
    if not check_user(token):
        return make_response(jsonify(message='请先登陆'), 400)

    item_id = get_request_args('item_id')
    items = query_db("SELECT * FROM item WHERE id=?", (item_id,), one=True)

    path = "static/img/itemImg/" + items['name'] + '/'
    img_list = []
    id = -1
    files = os.scandir(path)
    for file in files:
        if file.name.endswith("jpg") or file.name.endswith("png") or file.name.endswith("jpeg"):
            file_path = path + file.name
            data = {
                'uid': str(id),
                'url': file_path,
                'thumbUrl': file_path,
                'status': 'done',
                'name': file.name,
                'path': file_path
            }
            img_list.append(data)
            id -= 1

    return make_response(jsonify(img=img_list), 200)


@api.route('/api/get-detail-img', methods=['POST', 'GET'])
def get_detail_img():
    """
    获取detail photo
    :return:
    """
    token = get_header(request)
    if not check_user(token):
        return make_response(jsonify(message='请先登陆'), 400)

    item_id = get_request_args('item_id')
    items = query_db("SELECT * FROM item WHERE id=?", (item_id,), one=True)

    path = "static/img/discriptions/" + items['name'] + '/'
    img_list = []
    id = -1
    files = os.scandir(path)
    for file in files:
        if file.name.endswith("jpg") or file.name.endswith("png") or file.name.endswith("jpeg"):
            file_path = path + file.name
            data = {
                'uid': id,
                'url': file_path,
                'thumbUrl': file_path,
                'status': 'done',
                'name': file.name,
                'path': file_path
            }
            img_list.append(data)
            id -= 1

    return make_response(jsonify(img=img_list), 200)


@api.route('/api/get-detail-by-id', methods=['POST', 'GET'])
def get_main_details():
    """
    获取物品详细信息
    :return:
    """
    token = get_header(request)
    if not check_user(token):
        return make_response(jsonify(message='请先登陆'), 400)

    item_id = get_request_args('item_id')
    items = query_db("SELECT * FROM item WHERE id=?", (item_id,), one=True)
    types = query_db("SELECT * FROM item_price WHERE item=?", (items['id'],))
    items['types'] = types

    return make_response(jsonify(data=items), 200)


@api.route('/api/delete-photo', methods=['POST', 'GET'])
def delete_photo():
    """
    删除本地照片
    :return:
    """
    token = get_header(request)
    if not check_user(token):
        return make_response(jsonify(message='请先登陆'), 400)

    # 判断文件是否存在，如果存在删除
    file_path = get_request_args('file_path')
    if os.path.exists(file_path):
        os.remove(file_path)

    return make_response(jsonify(message='删除成功'), 200)


@api.route('/api/update-item',  methods=['POST', 'GET'])
def update_item():
    """
    更新商品信息
    :return:
    """
    token = get_header(request)
    if not check_user(token):
        return make_response(jsonify(message='请先登陆'), 400)

    item_id = get_request_args('item_id')
    item_name = get_request_args('name')
    tags = get_request_args('tags')
    weight = get_request_args('weight')
    product_name = get_request_args('product_name')

    main_img = get_request_file('mains', required=False)
    detail_img = get_request_file('details', required=False)

    query_db("UPDATE item SET name=?, tags=?, weight=?,product_name=? WHERE id=?",
             (item_name, tags, weight, product_name, item_id))

    if main_img is not None:
        for mg in main_img:
            if mg and check_allow(mg.filename):
                target = "static/img/itemImg/%s" % item_name
                if not os.path.isdir(target):
                    os.mkdir(target)

                filepath = target + "/main.jpg"
                mg.save(filepath)

    if detail_img is not None:
        for dg in detail_img:
            if dg and check_allow(dg.filename):
                target = "static/img/discriptions/%s" % item_name
                if not os.path.isdir(target):
                    os.mkdir(target)

                filepath = target + "/%s" % dg.filename
                dg.save(filepath)

    return make_response(jsonify(message='更新成功'), 200)


@api.route('/api/get-all-item-id', methods=['POST', 'GET'])
def get_all_item_id():
    """
    获取所有的item id来做autocomplete
    :return:
    """
    token = get_header(request)
    if not check_user(token):
        return make_response(jsonify(message='请先登陆'), 400)
    items = query_db("SELECT id FROM item")
    id = []
    for item in items:
        id.append(str(item['id']))

    return make_response(jsonify(id=id), 200)


@api.route('/api/add-item-type', methods=['POST', 'GET'])
def add_item_type():
    """
    添加商品的价格类型
    比如三罐包邮等
    :return:
    """
    token = get_header(request)
    if not check_user(token):
        return make_response(jsonify(message='请先登陆'), 400)

    item_id = get_request_args('item_id')
    item_type = get_request_args('item_type')
    item_price = get_request_args('item_price')

    t = query_db("SELECT * FROM item_price WHERE item=? AND price_type=?",
                 (item_id, item_type), one=True)

    if t is not None:
        return make_response(jsonify(message='类型已存在'), 200)

    query_db("INSERT INTO item_price(item, price_type, price) VALUES (?,?,?)",
             (item_id, item_type, item_price))

    return make_response(jsonify(message='添加成功'), 200)
