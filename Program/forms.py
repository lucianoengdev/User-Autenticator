from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Length, DataRequired


class registro(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    user = StringField('Nome de Usuário', validators=[Length(max=15), DataRequired()])
    password1 = StringField('Senha', validators=[Length(min=6, max=12), DataRequired()])
    password2 = StringField('Confirme sua senha', validators=[Length(min=6, max=12), DataRequired()])

