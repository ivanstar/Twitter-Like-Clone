import flask
from flask import Flask, request, jsonify, g, current_app
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

#DATABASE = 'database.db'
#DEBUG = True

#app = Flask(__name__)
#app.config.from_object(__name__)
app = Flask('app')
app.config.from_envvar('APP_CONFIG')

#Function to help return json fomrat  
#Similar to api_users just to help return in json format 
def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


#Following functions create the custom command for flask init that runs the schema and creates database
def get_db():
    db = getattr(g,'_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = make_dicts
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv
    
@app.cli.command('init')
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


#This can be commented out. Not really needed for the project
@app.route('/', methods=['GET'])
def gome():
    return "<h1>Microservice for Users</h1><p>This is the microservice for the users</p>"


#Return all available users in the database
@app.route('/users/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = make_dicts
    cur = conn.cursor()
    all_users = cur.execute('SELECT * FROM USERS;').fetchall()

    return jsonify(all_users), 201


#Registers a new user to the database
@app.route('/register', methods=['POST'])
def createUser():
    userInfo = request.get_json()
    username = userInfo.get('username')
    email = userInfo.get('email')
    password = userInfo.get('password')
    hashed_password = generate_password_hash(password)
    
    conn = sqlite3.connect(app.config['DATABASE'])
    cur = conn.cursor()
    cur.execute('INSERT INTO USERS VALUES(?,?,?)', (username, email, hashed_password))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(message=username + ' was registered successfully.'), 201 


#Logs in a user by comparing the username and password given with the username and password in the database 
@app.route('/login', methods=['POST'])
def authenticateUser():
    userInfo = request.get_json()
    username = userInfo.get('username')
    password = userInfo.get('password')
    conn = sqlite3.connect(app.config['DATABASE'])
    cur = conn.cursor()
    userPassword = cur.execute('SELECT PASSWORD FROM USERS WHERE USERNAME = ?', [username]).fetchone()[0]
    
    if check_password_hash(userPassword, password):
        return jsonify(message=username + ' was authenticated successfully.'), 201 
    else:
        return jsonify(message=username + ' password incorrect' ), 401 


#Adds a new follower to the username given
@app.route('/follow', methods=['PUT'])
def addFollower():
    userInfo = request.get_json()
    username = userInfo.get('username')
    usernameToFollow = userInfo.get('usernameToFollow')
    
    conn = sqlite3.connect(app.config['DATABASE'])
    cur = conn.cursor()
    cur.execute('INSERT INTO FOLLOWERS (FOLLOWING, USER) VALUES(?,?)',(usernameToFollow, username))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify(message=username + ' is now following ' + usernameToFollow), 200


#Stop following a user.
@app.route('/unfollow', methods=['POST'])
def removeFollower():
    userInfo = request.get_json()
    username = userInfo.get('username')
    usernameToRemove = userInfo.get('usernameToRemove')
    
    conn = sqlite3.connect(app.config['DATABASE'])
    cur = conn.cursor()
    cur.execute('DELETE FROM FOLLOWERS WHERE USER = ? AND FOLLOWING = ?',(username, usernameToRemove))
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify(message=username + ' is now unfollowing ' + usernameToRemove),200



#Error checking
@app.errorhandler(404)
def page_not_found(e):
    return '''<h1>404</h1>
    <p>The resource could not be found.</p>''', 404

