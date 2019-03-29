from flask import Flask, render_template

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


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0',debug=True)
