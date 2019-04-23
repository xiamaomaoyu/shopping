from flask import Flask, render_template,jsonify
from datetime import  datetime

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("homepage.html")


@app.route('/cart')
def mycart():
    return render_template("cart.html")

@app.route('/chat')
def mychat():
    return render_template("chat.html")

@app.route('/item')
def item():
    return render_template("item.html")

@app.route('/user')
def user():
    return render_template("user.html")

@app.route('/orders')
def orders():
    return render_template("orders.html")

@app.route('/webHomepage')
def webHomepage():
    return render_template("webHomepage.html")

@app.route('/getTime', methods=["POST","GET"])
def getTime():
    ret = jsonify(datetime.now())
    return ret

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,session_id')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,HEAD')
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == '__main__':
    app.run(port=80, host='0.0.0.0')
