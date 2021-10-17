from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .functions import *
from .models import ProfileStudent


@api_view(['POST'])
def index(request):
    response = {
        'version': request.data.get('version'),
        'session': request.data.get('session'),
        'response': {
            'end_session': False
        }
    }
    user_id = str(request.data.get('session').get('user').get('user_id'))
    command = str(request.data.get('request').get('command').lower())
    session = bool(request.data.get('session').get('new'))
    exists = ProfileStudent.objects.filter(user_id=user_id).exists()

    if not exists and not similarity('настроить профиль', command):
        if similarity('помощь', command):
            response['response']['text'] = HELP
            return response
        response['response']['text'] = FIRST_START if session else FIRST_START_RETRY
        return Response(response)
    
    user = get_object_or_404(ProfileStudent, user_id=user_id) if exists else None
    if session and exists:
        if user.state == 'Complete':
            response['response']['text'] = GREETING.format(name=user.name)
            return Response(response)

    response['response']['text'] = handler(command, user, user_id, session)
    return Response(response)        

def handler(command: str, user: object, user_id, session):
    state = user.state if user is not None else None

    if session and state == 'Complete':
        return 'Привет! Если вы хотите узнать команды, то скажите мне "Команды"'

    if similarity('настроить профиль', command) or  \
        similarity('настройка профиля', command) or  \
        similarity('настроить', command) or  \
        similarity('настроить заново', command):
        return create_profile(command, user, user_id, state, session, need=True)

    if 'create_profile:' in state:
        return create_profile(command, user, user_id, state, session)
    
    if similarity('на сегодня', command) or  \
        similarity('расписание на сегодня', command) or  \
        similarity('пары на сегодня', command) or  \
        similarity('сегодня', command):
        return get_schedule_today_tomorrow(user)
    
    if similarity('на завтра', command) or  \
        similarity('расписание на завтра', command) or  \
        similarity('пары на завтра', command) or  \
        similarity('завтра', command):
        return get_schedule_today_tomorrow(user, _today=False)

    if similarity('команды', command) or  \
        similarity('какие есть команды', command) or  \
        similarity('все команды', command) or  \
        similarity('помощь', command):
        return COMMANDS
    
    if 'пары через' in command or  \
        'через' in command:
        return get_schedule_after_before_days(user, command)
    
    if 'пары были' in command or  \
        'дней назад' in command or  \
        'дня назад' in command or  \
        'день назад':
        return get_schedule_after_before_days(user, command, after=False)

    if similarity('какая пара сейчас', command) or  \
        similarity('сейчас', command) or  \
        similarity('пара сейчас', command or  \
        similarity('скоро', command) or  \
        similarity('какая пара скоро', command) or  \
        similarity('какая пара будет скоро', command) or  \
        similarity('какая пара в ближайшее время', command) or  \
        similarity('какая пара будет в ближайшее время', command) or  \
        similarity('в ближайшее время', command) or  \
        similarity('ближайшее время', command) or  \
        similarity('пара в ближайшее время', command)):
        return get_schedule_now(user)
    
    return 'Такой команды нет, чтобы узнать команды, скажите мне "Команды"'
