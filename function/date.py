from datetime import datetime

def get_day_of_week():
    weekday_list = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']

    weekday = weekday_list[datetime.today().weekday()]
    date = datetime.today().strftime("%Y년 %m월 %d일")
    result = ':calendar: 오늘은 {}({})입니다.'.format(date, weekday)
    return result

def get_time():
    result = ':clock9: 현재 시간은 {}입니다.'.format(datetime.today().strftime("%H시 %M분 %S초"))
    return result


def get_test(ts):
    return '{}'.format(ts)