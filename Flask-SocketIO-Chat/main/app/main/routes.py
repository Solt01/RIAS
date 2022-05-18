from flask import session, redirect, url_for, render_template, request
from . import main
from .forms import LoginForm
from . import events

@main.route('/getChat')
def getMsg():
    return events.retChat()

'''@main.route('/sendMessage/<user>')
def sendMsg(user):
    events.text(user)'''

@main.route('/', methods=['GET', 'POST'])
def index():
    # Форма входа в систему для входа в комнату.
    form = LoginForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.room.data
        return redirect(url_for('.chat'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')
    return render_template('index.html', form=form)


@main.route('/chat')
def chat():
    #Комната чата. Имя пользователя и номер должны быть сохранены в сеансе.
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room=room)
