from flask import session, redirect, url_for, request, render_template

from mongodb_api import mongo_client


def change_texts():
    if 'username' not in session:
        return redirect(url_for('login_page'))

    if request.method == 'GET':
        texts = mongo_client.get_texts()
        return render_template('change_texts.html', texts=texts)