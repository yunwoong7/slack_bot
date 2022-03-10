import json
from datetime import datetime
from flask import Flask, request, make_response
from slack_sdk import WebClient
from config import get_config
from function import *

_config = get_config()

token = _config['token']
app = Flask(__name__)
client = WebClient(token)


def event_handler(event_type, slack_event):
    channel = slack_event["event"]["channel"]
    string_slack_event = str(slack_event)

    if string_slack_event.find("{'type': 'user', 'user_id': ") != -1:
        try:
            if event_type == 'app_mention':
                query_word = slack_event['event']['blocks'][0]['elements'][0]['elements'][1]['text']
                user = slack_event['event']['user']
                ts = slack_event['event']['ts']
                answer = get_answer(query_word, user, ts)
                result = client.chat_postMessage(channel=channel,
                                                 text=answer)
            return make_response("ok", 200, )
        except IndexError:
            pass
    # Direct Call
    elif string_slack_event.find("'channel_type': 'im'") != -1:
        # print(string_slack_event)
        try:
            if slack_event['event']['client_msg_id']:
                query_word = slack_event['event']['text']
                user = slack_event['event']['user']
                ts = slack_event['event']['ts']
                answer = get_answer(query_word, user, ts)
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
        return make_response({"challenge": slack_event["challenge"]}, 200, {"content_type": "application/json"})

    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return event_handler(event_type, slack_event)
    return make_response("There are no slack request events", 404, {"X-Slack-No-Retry": 1})


if __name__ == '__main__':
    app.run(debug=True, port=5002)