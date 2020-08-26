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
    content = request.json
    user = content['username']
    password = content['password']
    if auth.VRify(user,password):
        print('User VRified!',user,password)
        return jsonify({'verified': '1','server':'vrdata.viarezo.fr'})
    return jsonify({'verified': '0'})

if __name__ == '__main__':
    auth = Auth()
    socketio.run(app,debug = True,host = "0.0.0.0",port = 80)


    
