FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
VERIFY_TOKEN='123p948dfjhakasiwsdfgwrfauewsdjk1234'
PAGE_ACCESS_TOKEN='EAASEOZClvJsIBAB6X23nhRWsZA9XblvAgaklpYwtyFiZCZAQW7iH2jIvQlP9wAGjZAfYBT7HBaEShugta9zOqYZBKO6ZARPZBOdmoLs4EqvBA2TbJuXNaqZCmVdNbbAZCfwBBGkqljWHkJSlfCbRnjhyw8vYse3cCZBQVxKdqunSIAr9wZDZD'



def is_user_message(message):
    print('is_user_message')
    """Check if the message is a message from the user"""
    return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo"))
