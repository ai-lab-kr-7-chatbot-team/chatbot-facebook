import os
from flask import Flask, request
import requests
from flask_restful import Api
from flask_jwt_extended import JWTManager
import config
from .models.db import mongo

import flask_api_demo.fbchat

telelgram_token = ""
f = open("flask_api_demo/.telelgram_token", 'r')
telelgram_token = f.readline()
telelgram_token = telelgram_token.rstrip(' \t\n\r')
f.close()

# print('telelgram_token= [',telelgram_token,']')


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

    @app.route("/telegram_listen", methods=['POST'])
    def telegram_listen():
        print('telegram called webhook  post')
        payload = request.get_json()
        print('payload =',payload)

        # payload = {'update_id': 280974475, 'message': {'message_id': 31, 'from': {'id': 43446854, 'is_bot': False, 'first_name': 'Roy', 'last_name': 'Cho', 'username': 'roy_cho', 'language_code': 'ko'}, 'chat': {'id': 43446854, 'first_name': 'Roy', 'last_name': 'Cho', 'username': 'roy_cho', 'type': 'private'}, 'date': 1606571726, 'text': 'hi'}}
        # payload = {'update_id': 280974479, 'edited_message': {'message_id': 40, 'from': {'id': 43446854, 'is_bot': False, 'first_name': 'Roy', 'last_name': 'Cho', 'username': 'roy_cho', 'language_code': 'ko'}, 'chat': {'id': 43446854, 'first_name': 'Roy', 'last_name': 'Cho', 'username': 'roy_cho', 'type': 'private'}, 'date': 1606572265, 'edit_date': 1606572312, 'text': 'hello'}}

        message = payload.get('message',None)
        if message is None:
            message = payload.get('edited_message',None)

        print('message = ',message)
        chatMsg = message['text']
        print('chatMsg =' ,chatMsg)
        url = "http://localhost:5001/bot?chat="+chatMsg # 챗봇에게 말을 건다.
        response = requests.get(url) # 챗봇의 출력 메세지 가져오기.

        # 챗봇 메세지(response) 를 다시 텔레그램에게 전달.
        url = "https://api.telegram.org/bot"+ telelgram_token + "/sendMessage?chat_id=43446854&text=" + response.text
        print('url=',url)
        response = requests.get(url) 
        print(response.status_code )
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
