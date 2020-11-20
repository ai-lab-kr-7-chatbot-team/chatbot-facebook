from flask import Flask, request
import requests
from flask_restful import Api
from flask_jwt_extended import JWTManager

import config
from .models.db import mongo

FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
VERIFY_TOKEN='123p948dfjhakasiwsdfgwrfauewsdjk1234'
PAGE_ACCESS_TOKEN='EAASEOZClvJsIBAB6X23nhRWsZA9XblvAgaklpYwtyFiZCZAQW7iH2jIvQlP9wAGjZAfYBT7HBaEShugta9zOqYZBKO6ZARPZBOdmoLs4EqvBA2TbJuXNaqZCmVdNbbAZCfwBBGkqljWHkJSlfCbRnjhyw8vYse3cCZBQVxKdqunSIAr9wZDZD'
# app id = 9405896757207019
# secret : 941c25ce5539aea839b0e18aab133c747
def send_message(recipient_id, text):
    """Send a response to Facebook"""
    payload = {
        'message': {
            'text': text
        },
        'recipient': {
            'id': recipient_id
        },
        'notification_type': 'regular'
    }

    auth = {
        'access_token': PAGE_ACCESS_TOKEN
    }

    response = requests.post(
        FB_API_URL,
        params=auth,
        json=payload
    )

    return response.json()

def get_bot_response(message):
    print('get_bot_response')
    """This is just a dummy function, returning a variation of what
    the user said. Replace this function with one connected to chatbot."""
    return "This is a dummy response to '{}'".format(message)


def verify_webhook(req):
    print('verify_webhook 1234',req.args)
    if req.args.get("hub.verify_token") == VERIFY_TOKEN:
        return req.args.get("hub.challenge")
    else:
        return "incorrect"

def respond(sender, message):
    print('respond')
    """Formulate a response to the user and
    pass it on to a function that sends it."""
    response = get_bot_response(message)
    send_message(sender, response)


def is_user_message(message):
    print('is_user_message')
    """Check if the message is a message from the user"""
    return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo"))


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    if app.config['ENV'] == 'development':
        app.config.from_object(config.DevelopmentConfig)
    elif app.config['ENV'] == 'testing':
        app.config.from_object(config.TestingConfig)
    elif app.config['ENV'] == 'production':
        app.config.from_object(config.ProductionConfig)
    else:
        raise ValueError('Check FLASK_ENV')

    app.config.from_pyfile('application.cfg')

    mongo.init_app(app)
    jwt = JWTManager(app)

    # ref. https://github.com/flask-restful/flask-restful/issues/280
    handle_exception = app.handle_exception
    handle_user_exception = app.handle_user_exception

    @app.route('/')
    def hello_world():
        print('hello called')
        return 'Hello, World!'    


    @app.route("/webhook", methods=['GET'])
    def listen():
        print('called webhook  get')
        """This is the main function flask uses to
        listen at the `/webhook` endpoint"""
        if request.method == 'GET':
            return verify_webhook(request)

    @app.route("/webhook", methods=['POST'])
    def talk():
        print('called webhook  post')
        payload = request.get_json()
        event = payload['entry'][0]['messaging']
        for x in event:
            if is_user_message(x):
                text = x['message']['text']
                sender_id = x['sender']['id']
                respond(sender_id, text)

        return "ok"

    from .resources.foo import (
        foo_bp,
        Hello,
        HelloSecret,
    )

    api_foo = Api(foo_bp)
    api_foo.add_resource(Hello, '/hello')
    api_foo.add_resource(HelloSecret, '/secret')

    app.register_blueprint(foo_bp)

    # ref. https://github.com/flask-restful/flask-restful/issues/280
    app.handle_exception = handle_exception
    app.handle_user_exception = handle_user_exception

    return app
