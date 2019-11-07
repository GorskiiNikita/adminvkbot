from flask import render_template, session, redirect, url_for, request
from mongodb_api import mongo_client


WEEKDAYS = [('1', 'Понедельник'),
            ('2', 'Вторник'),
            ('3', 'Среда'),
            ('4', 'Четверг'),
            ('5', 'Пятница'),
            ('6', 'Суббота')]

REVERSE_WEEKDAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
LESSONS = ['first', 'second', 'third', 'fourth', 'fifth']

LESSONS_TIME = (('1',  '9:00 - 10:30'),
                ('2',  '10:45 - 12:15'),
                ('3',  '12:30 - 14:00'),
                ('4',  '15:00 - 16:30'),
                ('5',  '16:45 - 18:15'))


def update_group(key):
    if 'username' not in session:
        return redirect(url_for('login_page'))
    if request.method == 'GET':
        group_data = mongo_client.get_group(key)
        resp = {}
        for i in range(6):
            for j in range(5):
                if group_data[REVERSE_WEEKDAYS[i]][LESSONS[j]] is None:
                    resp[f'{i+1}_{j+1}_numerator'] = ''
                    resp[f'{i + 1}_{j + 1}_denumerator'] = ''
                    resp[f'{i + 1}_{j + 1}_wherenumerator'] = ''
                    resp[f'{i + 1}_{j + 1}_wheredenumerator'] = ''
                    continue

                if group_data[REVERSE_WEEKDAYS[i]][LESSONS[j]][0] is None:
                    resp[f'{i + 1}_{j + 1}_numerator'] = ''
                    resp[f'{i + 1}_{j + 1}_wherenumerator'] = ''
                else:
                    resp[f'{i + 1}_{j + 1}_numerator'] = group_data[REVERSE_WEEKDAYS[i]][LESSONS[j]][0]['name']
                    resp[f'{i + 1}_{j + 1}_wherenumerator'] = group_data[REVERSE_WEEKDAYS[i]][LESSONS[j]][0]['where']

                if group_data[REVERSE_WEEKDAYS[i]][LESSONS[j]][1] is None:
                    resp[f'{i + 1}_{j + 1}_denumerator'] = ''
                    resp[f'{i + 1}_{j + 1}_wheredenumerator'] = ''
                else:
                    resp[f'{i + 1}_{j + 1}_denumerator'] = group_data[REVERSE_WEEKDAYS[i]][LESSONS[j]][1]['name']
                    resp[f'{i + 1}_{j + 1}_wheredenumerator'] = group_data[REVERSE_WEEKDAYS[i]][LESSONS[j]][1]['where']

        return render_template('update_page.html', weekdays=WEEKDAYS, lessons=LESSONS_TIME, data=resp, group_id=key)

    group_data = dict(request.form)
    entry = {'_id': key,
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
            numerator = group_data[f'{i + 1}_{j + 1}_numerator']
            denumerator = group_data[f'{i + 1}_{j + 1}_denumerator']
            if numerator == '' and denumerator == '':
                continue
            elif numerator != '' and denumerator == '':
                entry[REVERSE_WEEKDAYS[i]][LESSONS[j]] = [
                    {'name': numerator, 'where': group_data[f'{i + 1}_{j + 1}_wherenumerator']},
                    None]
            elif numerator == '' and denumerator != '':
                entry[REVERSE_WEEKDAYS[i]][LESSONS[j]] = [None,
                                                          {'name': denumerator,
                                                           'where': group_data[f'{i + 1}_{j + 1}_wheredenumerator']}]
            else:
                entry[REVERSE_WEEKDAYS[i]][LESSONS[j]] = [
                    {'name': numerator, 'where': group_data[f'{i + 1}_{j + 1}_wherenumerator']},
                    {'name': denumerator, 'where': group_data[f'{i + 1}_{j + 1}_wheredenumerator']}]

    mongo_client.update_group(key, entry)
    return redirect(url_for('index_page'))
