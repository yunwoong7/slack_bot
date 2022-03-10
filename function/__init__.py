from function.date import *
from function.user import *
from function.info import *

def get_question(query_word):
    question_dict = {}
    _config = get_config()
    try:
        question_dict = _config['questions'][query_word]
    except KeyError:
        try:
            for question in _config['questions']:
                if query_word in _config['questions'][question]['synonym']:
                    question_dict = _config['questions'][question]
        except KeyError:
            pass

    return question_dict


def get_answer(query_word, user, ts):
    answer = ''
    question_dict = get_question(query_word.strip())

    if question_dict:
        func = question_dict['func']

        if func is None:
            answer = question_dict['answer']
        else:
            answer = eval('{}'.format(func))
    else:
        answer = "알 수 없는 질의입니다. 답변을 드릴 수 없습니다."

    return answer