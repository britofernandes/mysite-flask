from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, EmailField
from wtforms.validators import DataRequired, Email

class NameForm(FlaskForm):
    name = StringField('Qual é o seu nome?', validators=[DataRequired()])
    email = EmailField('Qual é o seu email (Envio de notificação do novo usuário)?', validators=[DataRequired(), Email()])
    prontuario = StringField('Qual é o seu prontuário?', validators=[DataRequired()])
    enviar_zoho = BooleanField('Enviar cópia para flaskaulasweb@zohomail.com?')
    submit = SubmitField('Submit')
