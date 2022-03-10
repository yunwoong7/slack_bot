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


def get_member():
    result = ":information_source: CheckMate 멤버는 총 4명입니다.\n" \
             "이메일\n" \
             "> 백승환 : ssennom0@naver.com, sh.baek@sk.com, keeper100@gmail.com\n" \
             "> 조경민 : km78cho@gmail.com, silverte@sk.com\n" \
             "> 최기형 : crossorbit@gmail.com, kihchoi@sk.com\n" \
             "> 김윤웅 : yunwoong7@gmail.com, yunwoong@sk.com\n" \
             "맥북\n" \
             "> 백승환 : SKCC19N00595       (A4-83-E7-4F-DE-6B)      10.250.84.80\n" \
             "> 조경민 : silverte                       ( F8:FF:C2:5C:E7:2E )       10.250.84.208\n" \
             "> 최기형 : SKCC19N01291       ( F8-FF-C2-2C-AA-50 )     10.250.85.130\n" \
             "> 김윤웅 : SKCC19N00318       ( 38-F9-D3-96-2C-4A )     10.250.85.4"

    return result