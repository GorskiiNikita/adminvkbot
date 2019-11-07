from flask import render_template, redirect, url_for, session
from mongodb_api import mongo_client


def index_page():
    if 'username' in session:
        list_of_groups = [group.upper() for group in mongo_client.get_list_of_groups()]
        return render_template('index.html', groups=list_of_groups)
    return redirect(url_for('login_page'))
