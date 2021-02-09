FLASK_ENV=development
APP_CONFIG=routes.cfg
#Project 5
#   Ivan Tu - ivanstar@csu.fullerton.edu

import flask
from flask import Flask, request, jsonify, g, current_app
import sqlite3
import time, datetime

#DATABASE = 'database.db'
#DEBUG = True

#app = flask.Flask(__name__)
#app.config.from_object(__name__)
app = Flask(__name__)
app.config.from_envvar('APP_CONFIG')


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

#Can also be commented out. Not needed for final project
@app.route('/', methods=['GET'])
def gome():
    return "<h1>Microservice for Users</h1><p>This is the microservice for the users</p>"


#Returns recent tweets from a user.
@app.route('/userTimeline', methods=['GET'])
def getUserTimeline():
    userInfo = request.get_json()
    username = userInfo.get('username')
    
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    userTimeline = cur.execute('SELECT * FROM TWEETS WHERE AUTHOR = ? LIMIT 25', (username)).fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(userTimeline), 201 


#Returns 25 tweets from all users
@app.route('/publicTimeline', methods=['GET'])
def getPublicTimeline():
    conn = sqlite3.connect('database.db')
    conn.row_factory = make_dicts
    cur = conn.cursor()
    recentTweets = cur.execute('SELECT * FROM TWEETS ORDER BY TIME_STAMP DESC LIMIT 25;').fetchall()

    return jsonify(recentTweets), 201


#Post a new tweet.
@app.route('/postTweet', methods=['POST'])
def postTweet():
    postTime = time.time()
    date = str(datetime.datetime.fromtimestamp(postTime).strftime('%Y-%m-%d %H:%M:%S'))

    tweetInfo = request.get_json()
    username = tweetInfo.get('username')
    tweetText = tweetInfo.get('tweet')
    
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO TWEETS (TWEET, TIME_STAMP, AUTHOR) VALUES(?,?,?)', (tweetText, date, username))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify(message= username + ' posted: ' + tweetText), 201


#Home Timeline aka the most recent tweets from your followers
@app.route('/homeTimeline', methods=['GET'])
def getHomeTimeline():
    userInfo = request.get_json()
    username = userInfo.get('username')
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = make_dicts
    cur = conn.cursor()
    homeTweets = cur.execute('SELECT TWEET,TIME_STAMP,AUTHOR FROM TWEETS INNER JOIN FOLLOWERS ON FOLLOWERS.FOLLOWING = TWEETS.AUTHOR WHERE FOLLOWERS.USER =? ORDER BY TIME_STAMP DESC LIMIT 25',(username)).fetchall()
    return jsonify(homeTweets), 201


#Error checking
@app.errorhandler(404)
def page_not_found(e):
    return '''<h1>404</h1>
    <p>The resource could not be found.</p>''', 404

