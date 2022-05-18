from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    #Принимает ник и номер.
    name = StringField('Имя', validators=[DataRequired()])
    room = StringField('Комната', validators=[DataRequired()])
    submit = SubmitField('Войти в комнату')
