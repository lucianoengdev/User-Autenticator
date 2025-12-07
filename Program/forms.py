from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import Length, DataRequired, EqualTo, NumberRange


class registro(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[Length(max=30), DataRequired()])
    password1 = StringField('Senha', validators=[Length(min=6, max=12), DataRequired()])
    password2 = StringField('Confirme sua senha', validators=[EqualTo('password1'), DataRequired()])

class CalculoFerroviario(FlaskForm):
    velocidade = FloatField('Velocidade Diretriz (V) [km/h]', validators=[DataRequired()])
    raio = FloatField('Raio da Curva (R) [m]', validators=[DataRequired()])
    bitola = FloatField('Bitola (b) [m]', validators=[DataRequired()])
    largura_boleto = FloatField('Largura do Boleto (Lb) [m]', validators=[DataRequired()])
    
    altura_cg = FloatField('Altura do CG (H) [m]', validators=[DataRequired()])
    coef_seguranca = FloatField('Coeficiente de Segurança (η)', validators=[DataRequired()], default=5.0)
    deslocamento_cg = FloatField('Deslocamento do CG (d) [m]', validators=[DataRequired()], default=0.1)
    
    aceleracao_jc = FloatField('Aceleração não compensada (Jc) [m/s²]', validators=[DataRequired()], default=0.65)
    gravidade = FloatField('Gravidade (g) [m/s²]', validators=[DataRequired()], default=9.81)
    
    submit = SubmitField('Calcular Superelevação')