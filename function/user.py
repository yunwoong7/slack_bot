from slack_sdk import WebClient
from config import get_config

_config = get_config()
token = _config['token']

client = WebClient(token)


def get_display_name(user):
    user_info = client.users_profile_get(user=user)

    return user_info.data['profile']['display_name']

def say_hello(user):
    display_name = get_display_name(user)
    result = ":hand: 안녕하세요. @{}. CheckMate입니다.".format(display_name)

    return result