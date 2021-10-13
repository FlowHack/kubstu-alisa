from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
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
    print(command)

    if not exists and not similarity('настроить профиль', command):
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

    if similarity('настроить профиль', command) or  \
        similarity('настройка профиля', command) or  \
        similarity('настроить', command) or  \
        similarity('настроить заново', command):
        return create_profile(command, user, user_id, state, session, need=True)

    if 'create_profile:' in state:
        return create_profile(command, user, user_id, state, session)

    if similarity('какая пара сейчас', command) or  \
        similarity('сейчас', command) or  \
        similarity('пара сейчас', command):
        pass
    
    if similarity('на сегодня', command) or  \
        similarity('расписание на сегодня', command) or  \
        similarity('пары на сегодня', command):
        pass
    
    if similarity('на завтра', command) or  \
        similarity('расписание на завтра', command) or  \
        similarity('пары на завтра', command):
        pass
