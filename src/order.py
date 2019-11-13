import src.db_hdl as DB
import datetime
import hashlib
import requests
import random
import calendar
import zeep
from zeep.transports import Transport
import xmltodict, json


key = '5dde5b629eac4dc688c83f9d4396b4a4'
m_number = '001007490'
m = hashlib.md5()


# 加密算法
def getMD5(timestamp, nonce_str):
    token = m_number + '&' + timestamp + '&' + nonce_str + '&' + key
    m.update(token.encode('utf-8'))
    return m.hexdigest()


def get_random(length):
    result = ''
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    characters = list(characters)
    charactersLength = len(characters)

    for i in range(0, length, 1):
        result += characters[random.randint(0,charactersLength-1)]

    return result


def add_order(phone_number):
    """
    We should add overall price into orders table.
    :param phone_number: the user phone number
    :return: the order id
    """
    max_id = DB.query_db("select max(order_id) from orders")[0]['max(order_id)']
    if max_id is None:
        max_id = 1
    receiver_id = DB.query_db("select receiver_detail from user where phone_number=?", (phone_number,))[0][
        'receiver_detail']
    receiver_detail = DB.query_db("select * from receiver_detail where id=?", (receiver_id,))[0]

    cart_records = DB.query_db("select * from cart_records where phone_number=?", (phone_number,))
    for record in cart_records:
        DB.query_db(
            "insert into orders(order_id, phone_number, item, item_price_type, quantity, receiver_name, receiver_address, receiver_phone, order_time, status) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (max_id + 1, phone_number, record['item'], record['item_price_type'], record['quantity'],
            receiver_detail['receiver_name'], receiver_detail['receiver_address'], receiver_detail['receiver_phone'], datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "unpaid"))
    return max_id + 1


def get_orders():
    result = []
    orders = DB.query_db("select * from orders")
    for order in orders:
        # print(order)
        item_name = DB.query_db("select name from item where id=?", (order['item'],))
        _order = {}
        for row in order:
            _order[row] = order[row]
        item_id = _order['item']
        _order['item'] = item_name[0]['name']
        _order['price'] = int(_order['quantity']) * int(DB.query_db("select price from item_price where item=? and price_type=?", (item_id, _order["item_price_type"]))[0]['price'])
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
        _order['price'] = int(_order['quantity']) * int(DB.query_db("select price from item_price where item=? and price_type=?", (item_id, _order["item_price_type"]))[0]['price'])
        result += [_order]
    return result


def get_order_by_phone_status(phone_number, status):
    result = {}
    orders = DB.query_db("select * from orders where phone_number=? and status=?", (phone_number, status))
    for order in orders:
        item_name = DB.query_db("select name from item where id=?", (order['item'],))
        _order = {}
        for row in order:
            _order[row] = order[row]
        item_id = _order['item']

        _order['item'] = item_name[0]['name']
        _order['price'] = int(_order['quantity']) * int(DB.query_db("select price from item_price where item=? and price_type=?", (item_id, _order["item_price_type"]))[0]['price'])
        id = _order["order_id"]
        if id in result:
            result[id].append(_order)
        else:
            result[id] = [_order]

    return list(result.values())


def set_order_status(order_id, status):
    DB.query_db("update orders set status=? where order_id=?", (status, order_id))


def set_order_comment(order_id, comment, rating):
    set_order_status(order_id, "closed")
    DB.query_db("INSERT INTO feedbacks(order_id, comment, rating) values (?, ?, ?)", (order_id, comment, rating))


def get_order_comment(order_id):
    return DB.query_db("select comment, rating from feedbacks where order_id=?", (order_id), one=True)


def get_all_orders():
    result = {}
    orders = DB.query_db("select * from orders")
    for order in orders:
        item_name = DB.query_db("select name from item where id=?", (order['item'],))
        _order = {}
        for row in order:
            _order[row] = order[row]
        item_id = _order['item']

        _order['item'] = item_name[0]['name']
        _order['price'] = int(_order['quantity']) * int(
            DB.query_db("select price from item_price where item=? and price_type=?",
                        (item_id, _order["item_price_type"]))[0]['price'])
        id = _order["order_id"]
        if id in result:
            result[id].append(_order)
        else:
            feedback = DB.query_db("select * from feedbacks where order_id = ?", (id, ))
            if len(feedback) != 0:
                result[id] = [feedback[0]["rating"], feedback[0]["comment"]]
            else:
                result[id] = ["", ""]
            result[id].append(_order)

    return list(result.values())


def add_pay_order_no(order_id, pay_no):
    DB.query_db("UPDATE orders SET order_no = '%s' WHERE order_id = '%s'" % (pay_no, order_id))


def get_overall_price(order_id):
    """
    get overall price according to order id
    :param order_id:
    :return:
    """
    overall_price = 0
    orders = DB.query_db("SELECT * FROM orders WHERE order_id='%s'" % order_id)

    for order in orders:
        price = DB.query_db("SELECT price FROM item_price WHERE item = '%s' AND price_type = '%s'" %
                            (order['item'], order['item_price_type']))
        overall_price += float(price[0]['price']) * order['quantity']

    return overall_price


def get_stock(receiver, address, phone, command, items):
    """
    get the delivery input xml information
    :param receiver: 收件人
    :param address: 收件人地址
    :param phone: 收件人电话
    :param command: 备注
    :param items: 商品
    :return: xml
    """
    stock = "<?xml version='1.0' encoding='UTF-8' standalone='no'?>"
    stock += "<ydjbxx>"
    stock += "<chrusername>test</chrusername>"
    stock += "<chrstockcode>au</chrstockcode>"
    stock += "<chrpassword>Test4567</chrpassword>"
    stock +="<chrjckrq>%s</chrjckrq>" % datetime.date.today()
    stock +="<chrzl>0</chrzl>"
    stock += "<chrsjr>%s</chrsjr>" % receiver
    stock += "<chrsjrdz>%s</chrsjrdz>" % address
    stock += "<chrsjrdh>%s</chrsjrdh>" % phone
    stock += "<chrjjr>lsy</chrjjr>"
    stock += "<chrjjrdh>0413164212</chrjjrdh>"
    stock += "<chrsfzhm>411627199808126417</chrsfzhm>"
    stock += "<chrbz>%s</chrbz>" % command
    stock += "<ydhwxxlist>"

    for item in items:
        stock += "<ydhwxx>"
        stock += "<chrpm>%s</chrpm>" % item['name']
        stock += "<chrpp>德运</chrpp>"
        stock += "<chrggxh>900g</chrggxh>"
        stock += "<chrjz>50.00</chrjz>"
        stock += "<chrjs>%s</chrjs>" % item['quantity']
        stock += "</ydhwxx>"

    stock += "</ydhwxxlist>"
    stock += "</ydjbxx>"

    return stock


def check_pay(order_id):
    """
    it will check whether the payment order is correct
    if correct then make a delivery
    otherwise do nothing
    :param order_id:
    :return:
    """
    order = DB.query_db("SELECT * FROM orders WHERE order_id = '%s'" % order_id)
    pay_no = order[0]['order_no']

    if pay_no is None or pay_no == '':
        return False

    dt = datetime.datetime.utcnow()
    timestamp = calendar.timegm(dt.utctimetuple())
    timestamp = str(timestamp)
    nonce_str = get_random(20)

    url = 'https://www.omipay.com.cn/omipay/api/v2/QueryOrder?'
    url += 'm_number=' + m_number
    url += '&timestamp=' + timestamp
    url += '&nonce_str=' + nonce_str
    url += '&sign=' + getMD5(timestamp, nonce_str)
    url += '&order_no=' + pay_no

    response = requests.get(
        url=url
    )

    response.raise_for_status()
    res = response.json()
    # if the pay is finished, then delivery
    if res['result_code'] == 'PAID':
        # set the order status unsent, and then make the delivery
        check = DB.query_db("SELECT * FROM orders WHERE order_id='%s'" % order_id)
        if check[0]['status'] == 'sent' or check[0]['delivery_no'] != '':
            return False
        DB.query_db("UPDATE orders SET status = 'unsent' WHERE order_id = '%s'" % order_id)
        # get all the items of this order
        items = []
        for o in order:
            item = DB.query_db("SELECT * FROM item WHERE id = '%s'" % o['item'])
            item[0]['quantity'] = o['quantity']
            items.append(item[0])

        stock = get_stock(order[0]['receiver_name'], order[0]['receiver_address'], order[0]['receiver_phone'],
                          'nothing', items)
        transport = Transport(timeout=10)
        wsdl = 'http://www.zhonghuan.com.au:8085/API/cxf/au/recordservice?wsdl'
        client = zeep.Client(wsdl=wsdl, transport=transport)
        result = client.service.getRecord(stock)
        print(result)
        if result['msgtype'] == '200':
            delivery_id = result['chrfydh']
            print(delivery_id)
            DB.query_db("UPDATE orders SET delivery_no = '%s' AND status='sent' WHERE order_id = '%s'" % (delivery_id, order_id))

        return True
    return False


def check_delivery_id(order_id):
    """
    get the delivery history according to order id
    :param order_id: which need to be checked
    :return: delivery history json style
    """
    order = DB.query_db("SELECT * FROM orders WHERE order_id='%s'" % order_id)
    delivery_id  = order[0]['delivery_no']

    if delivery_id is None or delivery_id == '':
        return None

    wsdl = 'http://www.zhonghuan.com.au:8085/API/cxf/common/logisticsservice?wsdl'
    client = zeep.Client(wsdl=wsdl)
    result = client.service.getLogisticsInformation(delivery_id, 'au')

    o = xmltodict.parse(result)
    data = json.dumps(o, ensure_ascii=False).encode('utf8')
    return data.decode()

