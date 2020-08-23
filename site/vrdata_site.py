from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
from flask_bootstrap import Bootstrap
from auth import Auth

app = Flask(__name__)
app.secret_key = 'super secret key'
socketio = SocketIO(app)
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/multicast/<string:code>', methods=['GET', 'POST'])
def multicast(code):
    if request.method == 'POST':
        content = request.json
        if not 'id' in content:
            #print('[PROBLEM]',content)
            return jsonify({})
        else:
            #print(code,content['id'])
            with app.app_context():
                socketio.emit('multicast', {request.get_json()}, broadcast = True,namespace='/'+code)
            return jsonify({"code":code,"id":content['id']})
    return '''
    <!doctype html>
    <title>Use a HTTP POST Request</title>
    '''

@app.route('/query/<string:code>', methods=['GET', 'POST'])
def query(code):
    if request.method == 'POST':
        content = request.json
        if not 'id' in content:
            #print('[PROBLEM]',content)
            return jsonify({})
        else:
            #print(code,content['id'])
            with app.app_context():
                socketio.emit('multicast', {request.get_json()}, broadcast = True,namespace='/'+code)
            return jsonify({"code":code,"id":content['id']})
    return '''
    <!doctype html>
    <title>Use a HTTP POST Request</title>
    '''

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    content = request.json
    user = content['username']
    password = content['password']
    auth = Auth()
    if auth.VRify(user,password):
        print('User VRified!',user,password)
        #token = auth.token(user,password)
        #return jsonify({'token':token})
    return jsonify({'message': 'Wrong credentials'})

@socketio.on('code')
def handle_code(json, methods=['GET', 'POST']):
    socketio.emit('message', json,namespace='/a1b2c3')

if __name__ == '__main__':
    socketio.run(app,debug = True,host = "0.0.0.0",port = 80)


    
