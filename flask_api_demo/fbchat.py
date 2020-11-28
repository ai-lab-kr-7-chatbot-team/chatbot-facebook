from flask import Flask, request
import requests
from flask_restful import Api
from flask_jwt_extended import JWTManager
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





    # @app.route("/webhook", methods=['GET'])
    # def listen():
    #     print('called webhook  get')
    #     """This is the main function flask uses to
    #     listen at the `/webhook` endpoint"""
    #     if request.method == 'GET':
    #         return verify_webhook(request)

    # @app.route("/webhook", methods=['POST'])
    # def talk():
    #     print('called webhook  post')
    #     payload = request.get_json()
    #     event = payload['entry'][0]['messaging']
    #     for x in event:
    #         if is_user_message(x):
    #             text = x['message']['text']
    #             sender_id = x['sender']['id']
    #             respond(sender_id, text)

    #     return "ok"

