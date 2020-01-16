from flask_cors import CORS
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
CORS(app, supports_credentials=True)
socketio = SocketIO(app)


# @app.route('/staff/', methods=["POST", "GET"])
# def staff():
#     return render_template('staffChat.html')

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


@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response

if __name__ == '__main__':
    socketio.run(app,port=5000, host='0.0.0.0', debug=True)
