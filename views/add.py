from flask import render_template, session, redirect, url_for, request
from mongodb_api import mongo_client


WEEKDAYS = [(1, 'Понедельник'),
            (2, 'Вторник'),
            (3, 'Среда'),
            (4, 'Четверг'),
            (5, 'Пятница'),
            (6, 'Суббота')]

REVERSE_WEEKDAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
LESSONS = ['first', 'second', 'third', 'fourth', 'fifth']

LESSONS_TIME = ((1,  '9:00 - 10:30'),
                (2,  '10:45 - 12:15'),
                (3,  '12:30 - 14:00'),
                (4,  '15:00 - 16:30'),
                (5,  '16:45 - 18:15'))


def add_page():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    if request.method == 'GET':
        return render_template('add_group.html', weekdays=WEEKDAYS, lessons=LESSONS_TIME)
    group_data = dict(request.form)
    group_id = group_data.pop('group')

    entry = {'_id': request.form.get('group').lower(),
             'monday': {
                 'first': None,
                 'second': None,
                 'third': None,
                 'fourth': None,
                 'fifth': None,
             },
             'tuesday': {
                 'first': None,
                 'second': None,
                 'third': None,
                 'fourth': None,
                 'fifth': None
             },
             'wednesday': {
                 'first': None,
                 'second': None,
                 'third': None,
                 'fourth': None,
                 'fifth': None
             },
             'thursday': {
                 'first': None,
                 'second': None,
                 'third': None,
                 'fourth': None,
                 'fifth': None
             },
             'friday': {
                 'first': None,
                 'second': None,
                 'third': None,
                 'fourth': None,
                 'fifth': None
             },
             'saturday': {
                 'first': None,
                 'second': None,
                 'third': None,
                 'fourth': None,
                 'fifth': None}}

    for i in range(0, 6):
        for j in range(0, 5):
            numerator = group_data[f'{i+1}_{j+1}_numerator']
            denumerator = group_data[f'{i+1}_{j+1}_denumerator']
            if numerator == '' and denumerator == '':
                continue
            elif numerator != '' and denumerator == '':
                entry[REVERSE_WEEKDAYS[i]][LESSONS[j]] = [{'name': numerator, 'where': group_data[f'{i+1}_{j+1}_wherenumerator']},
                                                          None]
            elif numerator == '' and denumerator != '':
                entry[REVERSE_WEEKDAYS[i]][LESSONS[j]] = [None,
                                                         {'name': denumerator, 'where': group_data[f'{i + 1}_{j + 1}_wheredenumerator']}]
            else:
                entry[REVERSE_WEEKDAYS[i]][LESSONS[j]] = [{'name': numerator, 'where': group_data[f'{i + 1}_{j + 1}_wherenumerator']},
                                                          {'name': denumerator, 'where': group_data[f'{i + 1}_{j + 1}_wheredenumerator']}]

    mongo_client.add_group(entry)
    return redirect(url_for('index_page'))
