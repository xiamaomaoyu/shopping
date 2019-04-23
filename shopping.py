from flask import Flask, render_template,jsonify
from datetime import  datetime

app = Flask(__name__)
app.debug = 1
app.secret_key = 'development key'



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

@app.route('/getTime')
def getTime():
    ret = jsonify(datetime.now())
    return ret

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(port=5002, debug=1)
