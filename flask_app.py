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
    try:
        response = requests.post(
            current_app.config['API_URL'],
            auth=("api", current_app.config['API_KEY']),
            data={
                "from": current_app.config['API_FROM'],
                "to": to,
                "subject": f"{current_app.config['FLASKY_MAIL_SUBJECT_PREFIX']} {subject}",
                "text": text
            }
        )
        print("Email enviado:", response.status_code)
        return response
    except Exception as e:
        print("Erro ao enviar e-mail:", e)
        return None


class NameForm(FlaskForm):
    name = StringField('Qual é o seu nome?', validators=[DataRequired()])
    prontuario = StringField('Qual é o seu prontuário?', validators=[DataRequired()])
    email = EmailField('Qual é o seu e-mail (para notificação)?', validators=[DataRequired()])
    enviar_zoho = BooleanField('Enviar também para flaskaulasweb@zohomail.com?')
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data, prontuario=form.prontuario.data)
            db.session.add(user)
            db.session.commit()

            corpo_email = (
                f"Novo usuário cadastrado:\n"
                f"Nome: {form.name.data}\n"
                f"Prontuário: {form.prontuario.data}\n"
                f"Usuário: {form.name.data}"
            )

            # Lista de destinatários
            destinatarios = [form.email.data]  # e-mail do usuário institucional
            if form.enviar_zoho.data:
                destinatarios.append("flaskaulasweb@zohomail.com")

            # e-mail do administrador
            destinatarios.append(app.config['FLASKY_ADMIN'])

            send_email(destinatarios, "Novo usuário cadastrado", corpo_email)
            session['known'] = False
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
