import json
from datetime import datetime
from flask import Flask, request, make_response
from slack_sdk import WebClient

token = "<< Your token >>"
app = Flask(__name__)
client = WebClient(token)


def get_day_of_week():
    weekday_list = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']

    weekday = weekday_list[datetime.today().weekday()]
    date = datetime.today().strftime("%Y년 %m월 %d일")
    result = '{}({})'.format(date, weekday)
    return result

def get_time():
    return datetime.today().strftime("%H시 %M분 %S초")


def get_answer(text):
    trim_text = text.replace(" ", "")

    answer_dict = {
        '안녕': '안녕하세요. CheckMate입니다.',
        '요일': ':calendar: 오늘은 {}입니다'.format(get_day_of_week()),
        '시간': ':clock9: 현재 시간은 {}입니다.'.format(get_time()),
    }

    if trim_text == '' or None:
        return "알 수 없는 질의입니다. 답변을 드릴 수 없습니다."
    elif trim_text in answer_dict.keys():
        return answer_dict[trim_text]
    else:
        for key in answer_dict.keys():  # 키에서 먼저 찾고
            if key.find(trim_text) != -1:
                return "연관 단어 [" + key + "]에 대한 답변입니다.\n" + answer_dict[key]

        for key in answer_dict.keys():  # 키가 없으면 본문에 검색
            if answer_dict[key].find(text[1:]) != -1:
                return "질문과 가장 유사한 질문 [" + key + "]에 대한 답변이에요.\n"+ answer_dict[key]

    return text + "은(는) 없는 질문입니다."


def event_handler(event_type, slack_event):
    channel = slack_event["event"]["channel"]
    string_slack_event = str(slack_event)

    if string_slack_event.find("{'type': 'user', 'user_id': ") != -1:
        try:
            if event_type == 'app_mention':
                user_query = slack_event['event']['blocks'][0]['elements'][0]['elements'][1]['text']
                answer = get_answer(user_query)
                result = client.chat_postMessage(channel=channel,
                                                 text=answer)
            return make_response("ok", 200, )
        except IndexError:
            pass
    # Direct Call
    elif string_slack_event.find("'channel_type': 'im'") != -1:
        try:
            if slack_event['event']['client_msg_id']:
                user_query = slack_event['event']['text']
                answer = get_answer(user_query)
                result = client.chat_postMessage(channel=channel,
                                                 text=answer)
                return make_response("ok", 200, )
        except IndexError:
            pass
        except KeyError:
            pass

    message = "[%s] cannot find event handler" % event_type

    return make_response(message, 200, {"X-Slack-No-Retry": 1})


@app.route('/', methods=['POST'])
def hello_there():
    slack_event = json.loads(request.data)
    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type": "application/json"})

    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return event_handler(event_type, slack_event)
    return make_response("There are no slack request events", 404, {"X-Slack-No-Retry": 1})


if __name__ == '__main__':
    app.run(debug=True, port=5002)