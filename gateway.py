#
# Simple API gateway in Python
#
# Inspired by <https://github.com/vishnuvardhan-kumar/loadbalancer.py>
#
#   $ python3 -m pip install Flask python-dotenv
#

#Project 5 - API Gateway for directmessaging, timeline, and user services.
#   Ivan Tu - ivanstar@csu.fullerton.edu

import sys
import itertools
from itertools import cycle
import flask
import requests
from flask import request
from flask import jsonify
from functools import wraps
from flask_basicauth import BasicAuth

app = flask.Flask(__name__)
basic_auth = BasicAuth(app)
app.config.from_envvar('APP_CONFIG')

upstream_users = app.config['UPSTREAM_USERS']
upstream_timeline = app.config['UPSTREAM_TIMELINE']
upstream_auth = app.config['UPSTREAM_AUTH']
upstream_dm = app.config['UPSTREAM_DM']

#Get user endpoints and routes
user_routes = upstream_users['user_routes']
user_url = upstream_users['user_endpoint']

#Get timeline endpoints and routes
timeline_routes = upstream_timeline['timeline_routes']
timeline_url = upstream_timeline['timeline_endpoint']

#Get dm endpoints and routes
dm_routes = upstream_dm['dm_routes']
dm_url = upstream_dm['dm_endpoint']

#Cycle address to mimic round-robin load balancing
user_cycle = itertools.cycle(user_routes)
timeline_cycle = itertools.cycle(timeline_routes)
dm_cycle = itertools.cycle(dm_routes)


#Function used to delete dead server
def del_deadserver(current, userroutes, timeroutes):
    if current in userroutes:
        userroutes.remove(current)
    elif current in timeroutes:
        timeroutes.remove(current)  

#Function used to check if user is authenticated
def login_auth(self, username, password):
    resp = requests.post(upstream_auth + '#
# Simple API gateway in Python
#
# Inspired by <https://github.com/vishnuvardhan-kumar/loadbalancer.py>
#
#   $ python3 -m pip install Flask python-dotenv
#

#Project 5 - API Gateway for directmessaging, timeline, and user services.
#   Ivan Tu - ivanstar@csu.fullerton.edu

import sys
import itertools
from itertools import cycle
import flask
import requests
from flask import request
from flask import jsonify
from functools import wraps
from flask_basicauth import BasicAuth

app = flask.Flask(__name__)
basic_auth = BasicAuth(app)
app.config.from_envvar('APP_CONFIG')

upstream_users = app.config['UPSTREAM_USERS']
upstream_timeline = app.config['UPSTREAM_TIMELINE']
upstream_auth = app.config['UPSTREAM_AUTH']
upstream_dm = app.config['UPSTREAM_DM']

#Get user endpoints and routes
user_routes = upstream_users['user_routes']
user_url = upstream_users['user_endpoint']

#Get timeline endpoints and routes
timeline_routes = upstream_timeline['timeline_routes']
timeline_url = upstream_timeline['timeline_endpoint']

#Get dm endpoints and routes
dm_routes = upstream_dm['dm_routes']
dm_url = upstream_dm['dm_endpoint']

#Cycle address to mimic round-robin load balancing
user_cycle = itertools.cycle(user_routes)
timeline_cycle = itertools.cycle(timeline_routes)
dm_cycle = itertools.cycle(dm_routes)


#Function used to delete dead server
def del_deadserver(current, userroutes, timeroutes):
    if current in userroutes:
        userroutes.remove(current)
    elif current in timeroutes:
        timeroutes.remove(current)  

#Function used to check if user is authenticated
def login_auth(self, username, password):
    resp = requests.post(upstream_auth + '/login', json={'username': username, 'password': password})
    if resp.status_code == 200 or resp.status_code == 201:
        return True
    else:
        return ({'WWW-Authenticate': 'Basic realm="Login Required"'})


BasicAuth.check_credentials = login_auth


@app.errorhandler(404)
@basic_auth.required
def route_page(err):
    
    #Print server logs to verify requests to gateway are routed to different instances of a service
    resp = flask.request.full_path
    #app.logger.debug(resp)

    if flask.request.full_path in timeline_url:
        all_cycle = next(timeline_cycle)
        app.logger.debug('Timeline Service')
        app.logger.debug(resp)
        app.logger.debug(all_cycle)

    elif flask.request.full_path in user_url:
        all_cycle = next(user_cycle)
        app.logger.debug('User Service')
        app.logger.debug(resp)
        app.logger.debug(all_cycle)
    else:
        all_cycle = next(dm_cycle)
        app.logger.debug('DM Service')
        app.logger.debug(resp)
        app.logger.debug(all_cycle)

    try:
        response = requests.request(
            flask.request.method,
            all_cycle + flask.request.full_path,
            data=flask.request.get_data(),
            headers=flask.request.headers,
            cookies=flask.request.cookies,
            stream=True,
        )
    except requests.exceptions.RequestException as e:
        
        #del_deadserver(all_cycle, user_routes, timeline_routes)
        #Remove dead servers
        if all_cycle in user_routes:
            user_routes.remove(all_cycle)
        elif all_cycle in timeline_routes:
            timeline_routes.remove(all_cycle)

        app.log_exception(sys.exc_info())
        return flask.json.jsonify({
            'method': e.request.method,
            'url': e.request.url,
            'exception': type(e).__name__,
        }), 503

    #Check if response failed with status code 500 then remove the server   
    if response.status_code >= 500:
        if all_cycle in user_routes:
            user_routes.remove(all_cycle)
        elif all_cycle in timeline_routes:
            timeline_routes.remove(all_cycle)


    
    

    headers = remove_item(
        response.headers,
        'Transfer-Encoding',
        'chunked'
    )

    return flask.Response(
        response=response.content,
        status=response.status_code,
        headers=headers,
        direct_passthrough=True,
    )


def remove_item(d, k, v):
    if k in d:
        if d[k].casefold() == v.casefold():
            del d[k]
    return dict(d)
