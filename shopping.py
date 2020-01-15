from flask import Flask, render_template,jsonify, redirect, url_for, request
from flask_login import LoginManager,login_user, current_user, logout_user, login_required
from src.user import get_user
from src.db_hdl import query_db
from api import api
import hashlib
from flask_cors import CORS
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.secret_key = 'development key'
app.register_blueprint(api)
login_manager = LoginManager()
login_manager.init_app(app)

CORS(app)

socketio = SocketIO(app)

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


@app.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "POST":
        if request.form['type'] == "password":
            phone_number = request.form['phone_number']
            password = request.form['password']
            row = query_db("SELECT password FROM user WHERE phone_number=? ;",(phone_number,),one=True)
            if row is None:
                return redirect(url_for('login'))
            if password == row['password']:
                login_user(get_user(phone_number))
                return redirect(url_for("index"))
            # TODO: else respond username or password incorrect
        elif request.form['type'] == "verification_code":
            phone_number = request.form['phone_number']
            verfication_code = request.form['verification_code']
            row = query_db("SELECT verification_code,nick_name FROM user WHERE phone_number=? ;",(phone_number,),one=True)
            if row is None:
                return redirect(url_for('login'))
            if verfication_code == row['verification_code']:
                if row["nick_name"] == "NEWUSER":
                    login_user(get_user(phone_number))
                    return render_template("register.html",phone_number=phone_number)
                else:
                    login_user(get_user(phone_number))
                    return redirect(url_for("index"))
            # TODO: else respond verification code incorrect
    return render_template("login.html")

# TODO: register


# @app.route('/staff/', methods=["POST", "GET"])
# def staff():
#     return render_template('staffChat.html')


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
#@login_required
def mycart():
    if current_user.is_anonymous == True:
        return redirect(url_for("login"))
    return render_template("cart.html",user=current_user)


@app.route('/chat')
@login_required
def mychat():
    return render_template("chat.html", user=current_user.get_id())


@app.route('/item/<id>')
def item(id):
    return render_template("item.html",id=id)


@app.route('/user')
#@login_required
def user():
    if current_user.is_anonymous == True:
        return redirect(url_for("login"))
    return render_template("user.html",user=current_user)


@app.route('/orders/<tab>')
def orders(tab):
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
    if current_user.is_anonymous:
        return redirect(url_for("login"))
    return render_template("userDetails.html")


@app.route('/pay/<order_id>/')
def pay(order_id):
    if current_user.is_anonymous:
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
def dashboard():
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
    return render_template("tracking.html", order_id=order_id)


@app.route('/pay/success/<order_id>/')
def check_pay(order_id):
    message = "Pay Success" + order_id
    return message


@app.route('/comment/<order_id>')
def comment(order_id):
    return render_template("comment.html",order_id=order_id)

@socketio.on('user post')
def handle_user_post(str, methods=['GET', 'POST']):
    socketio.emit('staff', str)


@socketio.on('staff post')
def handle_staff_post(str,  methods=['GET', 'POST']):
    user_id = str["user_id"]
    socketio.emit(user_id, str)


@socketio.on('leave')
def handle_user_leave(str, methods=['GET', 'POST']):
    socketio.emit('leave', str["user_id"])


if __name__ == '__main__':
    socketio.run(app, port=5000, debug=True)
    # app.run(port=5000, debug=True)
