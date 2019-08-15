from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
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


if __name__ == '__main__':
    socketio.run(app, debug=True,port=5000,host='0.0.0.0')