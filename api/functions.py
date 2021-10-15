from difflib import SequenceMatcher
from .models import ProfileStudent
import requests
from bs4 import BeautifulSoup
from .variables import *
import calendar

def similarity(need: str, text: str):
        matcher = SequenceMatcher(a=need, b=text).ratio()
        matcher = round(matcher, 3)

        return True if matcher > 0.888 else False

def get_semestr(day):
    if (12 >= day.month >= 9) or (day.month == 1) or (day.month == 2 and day.day <= 28):
        return 1
    if 3 <= day.month <= 5:
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

def schedule(name: list):
    schedule = {}
    day_now = ''
    para_now = ''
    variants_with_two_dot = ['Примечание: ', 'Аудитория: ', 'Преподаватель: ']
        
    for item in name:
        if item in DAYS:
            day_now = item
            schedule[item] = {}
            continue
        if 'пара' in item:
            value = item.split(' пара ')
            para = PARS_BY_NUMBER[value[0]] + ' парой'
            para_now = para
            value = value[1].split(') / ')
            _time = value[0][1:].split(' - ')
            time = 'c ' + _time[0] + ' до ' + _time[1]
            time_of = _time[0].split(':')
            time_of = time_of[0] + '.' + time_of[1]
            time_to = _time[1].split(':')
            time_to = time_to[0] + '.' + time_to[1]
            value = value[1].split(' / ')
            name = value[0]
            form = value[1]
            schedule[day_now][para] = {
                'time': time,
                'time_of': time_of,
                'time_to': time_to,
                'name': name,
                'form': form
            }
        for var in variants_with_two_dot:
            if var in item:
                value = item.split(': ')
                schedule[day_now][para_now][value[0]] = value[1]
                continue

    return schedule

def get_parity(day: int, month: int, year: int):
    calendar_ = calendar.TextCalendar(calendar.MONDAY)
    lines = calendar_.formatmonth(year, month).split('\n')
    days_by_week = [week.lstrip().split() for week in lines[2:]]
    str_day = str(day)
    day = None

    for index, week in enumerate(days_by_week):
        if str_day in week:
            day = index + 1
            break
    
    return day % 2

def get_schedule(user, _today=True, _day=None):
    for item, value in FACULTIES.items():
        if user.faculties.lower() in item:
            faculties = value
    
    day = today() if _today else tomorrow() if _day is None else _day
    course = user.course
    year_start_learn = int(user.year_start_learn)
    form_of_learn = user.form_of_learn.upper()
    direction = user.direction.upper()
    group = user.group
    year = today_year()
    semestr = get_semestr(day)
    url = URL.format(
        faculties=faculties, course=course, year_start_learn=year_start_learn, 
        form_of_learn=form_of_learn, direction=direction, group=group, 
        year=year, semestr=semestr
    )

    if _today:
        day = today()
        parity = get_parity(day.day, day.month, day.year)
        day = WEEKDAYS[today_weekday()]
    else:
        if _day is None:
            day = tomorrow()
            parity = get_parity(day.day, day.month, day.year)
            day = WEEKDAYS[tomorrow_weekday()]
        else:
            parity = get_parity(_day.day, _day.month, _day.year)
            day = WEEKDAYS[_day.weekday()]

    response = requests.get(url).text
    soup = BeautifulSoup(response, 'lxml')

    try:
        if parity == 1:
            week = soup.find('div', attrs={'id': 'collapse_n_1'}).text.strip().split('\n')
        else:
            week = soup.find('div', attrs={'id': 'collapse_n_2'}).text.strip().split('\n')
    except AttributeError:
        return None
    
    _schedule = schedule(week)
    try:
        return _schedule[day]
    except KeyError:
        return None

def get_schedule_now(user):
    _schedule = get_schedule(user)
    if _schedule is None:
        return 'Видмо завтра нет пар! Возможно, что вы просто неправильно  \
            заполнили данные профиля! Для настройки профиля скажите "Настроить профиль"'

    time = str_to_time(str(today_hour()) + '.' + str(today_minute()))
    nearest = False
    para = None
    
    for item, value in _schedule.items():
        time_of = str_to_time(value['time_of'])
        time_to = str_to_time(value['time_to'])
        if time_of <= time <= time_to:
            para = {item: value}
            break
    
    if para is None:
        time = time + str_to_time('0.30')
        for item, value in _schedule.items():
            time_of = str_to_time(value['time_of'])
            time_to = str_to_time(value['time_to'])

            if time_of <= time <= time_to:
                nearest = True
                para = {item: value}
                break
        
        if para is None:
            return 'Сейчас и в ближайшие пол часа нет пар.'
    
    number_para = {value:int(key) for key, value in PARS_BY_NUMBER.items()}
    number_para = PARS_BY_NAME[
        int(number_para[
            list(para.keys())[0].split(' ')[0]
            ])
    ]
    para = para[list(para.keys())[0]]

    start_response = 'Скоро начнётся ' if nearest else 'Сейчас идёт '

    name = value['name']
    form = 'Форма не указана' if value['form'] == '' else value['form']
    teacher = 'Преподаватель не указан' if value['Преподаватель'] == '' else value['Преподаватель']
    note = True if 'Примечание' in list(value.values()) else ''
    if note is True:
        note = '' if value['Примечание'] == '' else 'Примечание: ' + value['Примечание'] + '.'
    aud = None if value['Аудитория'] == '' else value['Аудитория'].split('-')
    cab = f' Кабинет {aud[1]}' if aud[1] != '' else ''
    aud = 'Аудитория не указана' if aud is None else CORPUS[aud[0]] + '.' + cab
    
    return start_response + f'number_para пара: {name}. Адрес: {aud}. Преподаватель: {teacher}. Форма: {form}. {note}'

def get_schedule_today_tomorrow(user, _today=True, after_day=None):
    if after_day is None:
        _schedule = get_schedule(user, _today)
    else:
        _schedule = get_schedule(user, _today, after_day)
    
    if _schedule is None:
        return 'Видмо завтра нет пар! Возможно, что вы просто неправильно  \
            заполнили данные профиля! Для настройки профиля скажите "Настроить профиль"'

    response = ''
    for key, value in _schedule.items():
        name = value['name']
        form = 'Форма не указана' if value['form'] == '' else value['form']
        teacher = 'Преподаватель не указан' if value['Преподаватель'] == '' else value['Преподаватель']
        note = True if 'Примечание' in list(value.values()) else ''
        if note is True:
            note = '' if value['Примечание'] == '' else 'Примечание: ' + value['Примечание'] + '.'
        aud = None if value['Аудитория'] == '' else value['Аудитория'].split('-')
        cab = f' Кабинет {aud[1]}' if aud[1] != '' else ''
        aud = 'Аудитория не указана' if aud is None else CORPUS[aud[0]] + '.' + cab

        response += key + f': {name}. Адрес: {aud}. Преподаватель: {teacher}. Форма: {form}. {note}\n\n'
    
    return response

def get_schedule_after_before_days(user, command, after=True):
    days = ''

    for i in str(command):
        try:
            days += str(int(i))
        except ValueError:
            continue

    if days == '':
        return 'Похоже, что я не смогла распознать через сколько дней вы хотите узнать расписание.'
    
    after_days = day_after_days(int(days)) if after else day_before_days(int(days))
    return get_schedule_today_tomorrow(user, _today=False, after_day=after_days)

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
                        
        command = int(command.strip())

        ProfileStudent.objects.filter(
            user_id=user_id
        ).update(group=command, state='Complete')
        return COMPLETE_SETTINGS
