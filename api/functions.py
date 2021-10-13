from difflib import SequenceMatcher
from .models import ProfileStudent
from .variables import *

def similarity(need: str, text: str):
        matcher = SequenceMatcher(a=need, b=text).ratio()
        matcher = round(matcher, 3)

        return True if matcher > 0.799 else False

def get_semestr():
    month = today_month()
    day = today_day()

    if (12 >= month <= 9) or (month == 1) or (month == 2 and day <= 28):
        return 1
    if 3 <= month <= 5:
        return 2
    
    return None

def get_course(year_start):
    year = int(str(today_year())[-2:])
    month = today_month()

    if year_start == year:
        return 1
    if year_start < year:
        course = year - year_start
        return course if month < 7 else course + 1
    return None

def create_profile(command: str, user: object, user_id: str, state:str, new=False, need=False):    
    if user is None:
        ProfileStudent.objects.create(
            user_id=user_id,
            state='create_profile:name'
        )
        return CREATE_PROFILE_NAME

    state = state.split(':')[1]

    if state == 'Complete' or need is True:
        ProfileStudent.objects.filter(user_id=user_id).delete()
        ProfileStudent.objects.create(
            user_id=user_id,
            state='create_profile:name'
        )
        return CREATE_PROFILE_NAME
    
    if state == 'name':
        if new:
            return NEW_CREATE_PROFILE[state] if new else CREATE_PROFILE[state]

        state = 'create_profile:' + 'faculties'
        command = command.strip().capitalize()

        ProfileStudent.objects.filter(
            user_id=user_id
        ).update(name=command, state=state)
        return CREATE_PROFILE['faculties']      
    if state == 'faculties':
        if new:
            return NEW_CREATE_PROFILE[state] if new else CREATE_PROFILE[state]

        state = 'create_profile:' + 'year_start_learn'
        command = command.strip()

        ProfileStudent.objects.filter(
            user_id=user_id
        ).update(faculties=command, state=state)
        return CREATE_PROFILE['year_start_learn']  
    if state == 'year_start_learn':
        if new:
            return NEW_CREATE_PROFILE[state] if new else CREATE_PROFILE[state]

        state = 'create_profile:' + 'form_of_learn'
        command = int(command.strip())

        course = get_course(command)
        if course is None:
            return COURSE_ERROR

        ProfileStudent.objects.filter(
            user_id=user_id
        ).update(year_start_learn=command, course=course, state=state)
        return CREATE_PROFILE['form_of_learn']
    if state == 'form_of_learn':
        if new:
            return NEW_CREATE_PROFILE[state] if new else CREATE_PROFILE[state]
        
        state = 'create_profile:' + 'direction'
        command = command.strip().upper()

        ProfileStudent.objects.filter(
            user_id=user_id
        ).update(form_of_learn=command, state=state)
        return CREATE_PROFILE['direction']  
    if state == 'direction':
        if new:
            return NEW_CREATE_PROFILE[state] if new else CREATE_PROFILE[state]
                
        state = 'create_profile:' + 'group'
        command = command.strip().upper()

        ProfileStudent.objects.filter(
            user_id=user_id
        ).update(direction=command, state=state)
        return CREATE_PROFILE['group']  
    if state == 'group':
        if new:
            return NEW_CREATE_PROFILE[state] if new else CREATE_PROFILE[state]
                        
        state = 'create_profile:' + state
        command = int(command.strip())

        ProfileStudent.objects.filter(
            user_id=user_id
        ).update(group=command, state=state)
        return COMPLETE_SETTINGS
