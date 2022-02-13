from app import app
from database import db
from flask_restful import Api,Resource,request
from flask import session
api = Api(app)

class Chat(Resource):
    def get(self):
        cur = db.cursor(dictionary = True)
        cur.execute('''SELECT message,username FROM users
                    JOIN messages USING(user_id)
                    ORDER BY message_date''')
        res = cur.fetchall()
        return res
    def post(self):
        message = request.form['enter']
        user_id = session['user_id']
        if message == '':
            return {'message': ''}
        cur = db.cursor(dictionary = True)
        cur.execute('''INSERT INTO messages (message,user_id) VALUES
                    (%s,%s)''',(message,user_id))
        db.commit()
        cur.execute(f'''SELECT username FROM users
                     WHERE user_id = "{user_id}"''')
        res = cur.fetchone()
        return {'message':message,'username': res['username']}
api.add_resource(Chat,'/message')

class Logging(Resource):
    def post(self):
        cur = db.cursor(dictionary = True)
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if email == '' or password == '' or username == '':
            return {'msg':'Do not leave any field empty'}
        msg = 'Invalid username or password or email'
        cur.execute(f'''SELECT user_id, username,user_password,email
                    FROM users
                    WHERE username = "{username}" AND user_password = "{password}"
                    AND email = "{email}"''')
        res = cur.fetchone()
        if not res:
            return {'msg': msg}
        id = res['user_id']
        session['user_id'] = id
        session['username'] = username
        session['password'] = password
        session['email'] = email
        
        return {'user': username,'password':password, 'email': email, 'user_id': id}
    def get(self):
        return {'username': session.get('username',''),'password': session.get('password','')}
api.add_resource(Logging,'/log')

class SignUp(Resource):
    def post(self):
        cur = db.cursor(dictionary = True)
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if email == '' or password == '' or username == '':
            return {'msg':'Do not leave any field empty'}
        cur.execute(f'''SELECT username,user_password,email FROM users 
                    WHERE username = "{username}"  ''')
        res = cur.fetchone()
        if res:
            return {'msg': 'Username Taken'}
        cur.execute(f'''INSERT INTO users (username,user_password,email)
                    values(%s, %s,%s)''',(username,password,email))
        db.commit()
        cur.execute(f'''SELECT user_id FROM users 
                    WHERE username = "{username}"  AND user_password = "{password}"
                    AND email = "{email}"  ''')
        id = cur.fetchone()
        session['user_id'] = id['user_id']
        session['username'] = username
        session['password'] = password
        session['email'] = email
        return {'username': username,'password':password,'email':email,
                    'user_id': id['user_id']}
api.add_resource(SignUp,'/register_api')