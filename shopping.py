from flask import Flask, render_template,jsonify, redirect, url_for, request, session
from flask_login import LoginManager,login_user, current_user, logout_user, login_required
from src.user import get_user, Admin
from src.db_hdl import query_db
from api import api
import hashlib
from flask_cors import CORS
from flask_socketio import SocketIO
import datetime

app = Flask(__name__)
app.secret_key = 'development key'
app.register_blueprint(api)
login_manager = LoginManager()
login_manager.init_app(app)

socketio = SocketIO(app, cors_allowed_origins='*')

CORS(app, resources={r"/*": {"origins": "*"}})


key = '5dde5b629eac4dc688c83f9d4396b4a4'
m_number = '001007490'
m = hashlib.md5()


# 加密算法
def getMD5(timestamp, nonce_str):
    token = m_number + '&' + timestamp + '&' + nonce_str + '&' + key
    m.update(token.encode('utf-8'))
    return m.hexdigest()


@login_manager.user_loader
def load_user(id):
    user = get_user(id)
    if user is None:
        return redirect(url_for('login'))
    return get_user(id)

@app.route('/update_password', methods=["POST", "GET"])
def updatePassword():
    return render_template("updatePassword.html")

@app.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "POST":
        if request.form['type'] == "password":
            phone_number = request.form['phone_number']
            if phone_number[0] == '0':
                phone_number = phone_number[1:]
            password = request.form['password']
            row = query_db("SELECT password FROM user WHERE phone_number=? ;",(phone_number,),one=True)
            if row is None:
                return render_template("login.html", first_error="手机号尚未注册")
            if password == row['password']:
                login_user(get_user(phone_number))
                return redirect(url_for("index"))
            else:
                return render_template("login.html", second_error="密码错误")
            # TODO: else respond username or password incorrect
        elif request.form['type'] == "verification_code":
            phone_number = request.form['phone_number']
            if len(phone_number) > 0 and phone_number[0] == '0':
                phone_number = phone_number[1:]
            verfication_code = request.form['verification_code']
            row = query_db("SELECT verification_code,nick_name FROM user WHERE phone_number=? ;",(phone_number,),one=True)
            if row is None:
                return render_template("login.html", first_error="手机号错误")
            if verfication_code == row['verification_code']:
                if row["nick_name"] == "NEWUSER":
                    login_user(get_user(phone_number))
                    return render_template("register.html",phone_number=phone_number)
                else:
                    login_user(get_user(phone_number))
                    return redirect(url_for("index"))
            else:
                return render_template("login.html", second_error="验证码错误")
            # TODO: else respond verification code incorrect
    return render_template("login.html")

# TODO: register


@app.route('/staff/', methods=["POST", "GET"])
def staff():
    return render_template('staffChat.html')

@app.route('/admin-login', methods=["POST", "GET"])
def admin_login():

    if request.method == "POST":
        row = query_db("SELECT password FROM admin WHERE admin_name=? ;", (request.form['admin_name'],), one=True)
        if row is None:
            return render_template("admin-login.html")
        elif row["password"] != request.form["password"]:
            return render_template("admin-login.html")
        else:
            login_user(Admin(request.form['admin_name']))
            return redirect(url_for("dashboard"))
    return render_template("admin-login.html")


@app.route('/logout', methods=["POST", "GET"])
#@login_required
def logout():
    if current_user.is_anonymous:
        return redirect(url_for("login"))
    logout_user()
    return redirect(url_for("login"))


@app.route('/')
def index():
    return render_template("homepage.html")


@app.route('/cart')
@login_required
def mycart():
    if current_user.is_anonymous is True:
        return redirect(url_for("login"))
    elif current_user.get_type() == "Admin":
        return redirect(url_for("dashboard"))
    return render_template("cart.html",user=current_user)


@app.route('/chat')
@login_required
def mychat():
    if current_user.is_anonymous is True:
        return redirect(url_for("login"))
    elif current_user.get_type() == "Admin":
        return redirect(url_for("staff"))
    return render_template("chat.html", user=current_user.get_id())


@app.route('/item/<id>')
def item(id):
    return render_template("item.html",id=id)


@app.route('/user')
#@login_required
def user():
    if current_user.is_anonymous is True:
        return redirect(url_for("login"))
    elif current_user.get_type() == "Admin":
        return redirect(url_for("dashboard"))
    return render_template("user.html",user=current_user)


@app.route('/orders/<tab>')
def orders(tab):
    # TODO only owner of the order or admin can see it
    if current_user.is_anonymous is True:
        return redirect(url_for("login"))
    elif current_user.get_type() == "Admin":
        return redirect(url_for("dashboard"))

    return render_template("orders.html",tab=tab)


@app.route('/webHomepage')
def webHomepage():
    return render_template("webHomepage.html")


@app.route('/webSearch/')
@app.route('/webSearch/<keyword>')
def webSearch(keyword=None):
    if not keyword:
        keyword = "A2二段"
    return render_template("webSearch.html",keyword=keyword)


@app.route('/address/')
def address():
    if current_user.is_anonymous is True:
        return redirect(url_for("login"))
    elif current_user.get_type() == "Admin":
        return redirect(url_for("dashboard"))
    return render_template("userDetails.html")


@app.route('/pay/<order_id>/')
def pay(order_id):
    if current_user.is_anonymous == True:
        return redirect(url_for("login"))
    return render_template("pay.html",user=current_user, order_id = order_id)


@app.route('/gettoken')
def get_token():
    if current_user.is_anonymous:
        return redirect(url_for("login"))
    timestamp = request.args.get('timestamp')
    nonce_str = request.args.get('nonce_str')
    token = getMD5(timestamp, nonce_str)
    return jsonify({'m_number': m_number, 'sign': token.upper()})


@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.get_type() != "Admin":
        return redirect(url_for("admin_login"))
    return render_template('dashboard.html')


@app.route('/search/')
@app.route('/search/<keyword>')
def search(keyword=None):
    if not keyword:
        keyword = "A2二段"
    return render_template("search.html",keyword=keyword)


@app.route('/user/address/controller/')
def addressController():
    return render_template("addressPage.html")


@app.route('/qrcode')
def qrcode():
    return render_template("qrCode.html")


@app.route('/tracking/<order_id>')
def tracking(order_id):
    # TODO only owner of the order or admin can see it
    return render_template("tracking.html", order_id=order_id)


@app.route('/pay/success/<order_id>/')
def check_pay(order_id):
    message = "Pay Success" + order_id
    return message


def check_time():
    d_time1 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '8:00', '%Y-%m-%d%H:%M')
    d_time2 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '18:00', '%Y-%m-%d%H:%M')
    n_time = datetime.datetime.now()
    if n_time > d_time1 and n_time < d_time2:
        return True
    return False


@app.route('/comment/<order_id>')
def comment(order_id):
    return render_template("comment.html",order_id=order_id)

@app.errorhandler(401)
def unauthorised_error(error):
    return redirect(url_for("login"))

@socketio.on('user post')
def handle_user_post(msg, methods=['GET', 'POST']):
    if check_time() is False and session.get('online') is None:
        handle_staff_post({
            'user_message': '客服不在线请稍后联系（自动回复）',
            'user_image': '',
            'user_id': msg['user_id'],
            'auto': 1
        })
        return
    socketio.emit('staff', msg)


@socketio.on('staff post')
def handle_staff_post(msg,  methods=['GET', 'POST']):
    # {'user_message': 'hello', 'user_image': '', 'user_id': '123'}
    if msg['auto'] != 1:
        session['online'] = True
    user_id = msg["user_id"]
    socketio.emit(user_id, msg)


@socketio.on('leave')
def handle_user_leave(str, methods=['GET', 'POST']):
    socketio.emit('leave', str["user_id"])


if __name__ == '__main__':
    socketio.run(app, port=80, host='0.0.0.0', debug=True)

