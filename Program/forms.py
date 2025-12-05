from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Length, DataRequired, EqualTo


class registro(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[Length(max=30), DataRequired()])
    password1 = StringField('Senha', validators=[Length(min=6, max=12), DataRequired()])
    password2 = StringField('Confirme sua senha', validators=[Equalto('password1'), DataRequired()])

