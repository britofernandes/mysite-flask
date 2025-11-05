import os
import requests
from threading import Thread
from flask import Flask, render_template, session, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.config['API_KEY'] = os.environ.get('API_KEY')
app.config['API_URL'] = os.environ.get('API_URL')
app.config['API_FROM'] = os.environ.get('API_FROM')
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'


bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)



class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    prontuario = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))



def send_email(to, subject, text):
    """
    Envia e-mail via Mailgun ou SendGrid usando requests.
    """
    print("Enviando e-mail...")
    print(f"To: {to}")
    print(f"Subject: {subject}")
    print(f"Text: {text}")

    try:
        resposta = requests.post(
            app.config['API_URL'],
            auth=("api", app.config['API_KEY']),
            data={
                "from": app.config['API_FROM'],
                "to": to,
                "subject": f"{app.config['FLASKY_MAIL_SUBJECT_PREFIX']} {subject}",
                "text": text
            }
        )
        print("Resposta:", resposta.status_code, resposta.text)
        return resposta
    except Exception as e:
        print("Erro no envio:", e)
        return None

class NameForm(FlaskForm):
    name = StringField('Qual é o seu nome?', validators=[DataRequired()])
    prontuario = StringField('Qual é o seu prontuário?', validators=[DataRequired()])
    email = EmailField('Qual é o seu email (Envio de notificação do novo usuário)?', validators=[DataRequired(), Email()])
    enviar_zoho = BooleanField('Deseja enviar e-mail para flaskaulasweb@zohomail.com?')
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
    user = User.query.filter_by(username=form.name.data).first()
    if user is None:
        user = User(username=form.name.data,
                    prontuario=form.prontuario.data,
                    email=form.email.data)
        db.session.add(user)
        db.session.commit()
        session['known'] = False

        corpo_email = (
            f"Novo usuário cadastrado no sistema Flasky!\n\n"
            f"Nome: {form.name.data}\n"
            f"Prontuário: {form.prontuario.data}\n"
            f"Usuário: {form.name.data}\n"
            f"E-mail: {form.email.data}"
        )

        destinatarios = [app.config['FLASKY_ADMIN'], form.email.data]
        if form.enviar_zoho.data:
            destinatarios.append("flaskaulasweb@zohomail.com")

        send_email(destinatarios, "Novo usuário cadastrado", corpo_email)
    else:
        session['known'] = True

    session['name'] = form.name.data
    return redirect(url_for('index'))

    users = User.query.all()
    return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('known', False), users=users, current_time=datetime.utcnow())


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)
