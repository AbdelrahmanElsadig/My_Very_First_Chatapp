from flask import Flask,redirect, render_template, url_for,request
from database import db
from api import api,session
from flask_socketio import SocketIO,send,emit
app = Flask(__name__)
app.secret_key = 'whatever'
api.init_app(app)
socketio = SocketIO(app,cors_allowed_origins="*")

@socketio.on('send_message')
def handleMessage(data):
    app.logger.info(data)
    emit('receive-message',{'msg':data['message'],'user':data['name']},broadcast=True)
    return {'msg':data['message'],'user':data['name']}


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/register')
def register():
    if session.get('username',False):
        return redirect('/chat_room')
    return render_template('register.html')


@app.route('/chat_room',methods=['POST','GET'])
def chat_room():
    data = {'username': session.get('username',None), 'password': session.get('password',None)}
    if  data['username'] == None and  data['password'] == None:
        return redirect('/login')
    return render_template('chat.html')


@app.route('/login')
def login():
    if session.get('username',None) != None:
        return redirect('/chat_room')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username',None)
    session.pop('password',None)
    session.pop('user_id',None)
    session.pop('email',None)
    return redirect('/login')


if __name__ == '__main__':
    socketio.run(app,debug=True)