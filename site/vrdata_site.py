from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
from flask_bootstrap import Bootstrap
from auth import Auth

app = Flask(__name__)
app.secret_key = 'viazero'
socketio = SocketIO(app)
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    try:
        content = request.json
        user, password, db_name = content['username'], content['password'], content['db_name']

        vr_token = auth.VRify(user,password)
        print(user,' VRified!')

        server, token = auth.create_session(user,password,db_name,vr_token)
        print('Session Created')

        return jsonify({'verified': '1','server':server,'token':token})

    except BaseException:
        pass
    
    return jsonify({'verified': '0'})


if __name__ == '__main__':
    auth = Auth()
    socketio.run(app,debug = True,host = "0.0.0.0",port = 80)


    
