from flask import Flask, render_template,jsonify
from datetime import  datetime
from api import api

app = Flask(__name__)
app.secret_key = 'development key'
app.register_blueprint(api)


@app.route('/')
def hello_world():
    return render_template("homepage.html")


@app.route('/cart')
def mycart():
    return render_template("cart.html")

@app.route('/chat')
def mychat():
    return render_template("chat.html")

@app.route('/item/<id>')
def item(id):
    return render_template("item.html",id=id)

@app.route('/user')
def user():
    return render_template("user.html")

@app.route('/orders')
def orders():
    return render_template("orders.html")

@app.route('/webHomepage')
def webHomepage():
    return render_template("webHomepage.html")

@app.route('/webSearch/')
@app.route('/webSearch/<keyword>')
def webSearch(keyword=None):
    if not keyword:
        keyword = "A2二段"
    return render_template("webSearch.html",keyword=keyword)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/search/')
@app.route('/search/<keyword>')
def search(keyword=None):
    if not keyword:
        keyword = "A2二段"
    return render_template("search.html",keyword=keyword)

if __name__ == '__main__':
    app.run(debug=True,port=5000)
