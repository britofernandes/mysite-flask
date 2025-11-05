import os
from datetime import datetime
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_migrate import Migrate
from models import db, User, Role
from forms import NameForm
from email_utils import send_email

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configurações Mailgun/SendGrid (via variáveis de ambiente)
app.config['API_KEY'] = os.environ.get('API_KEY')
app.config['API_URL'] = os.environ.get('API_URL')
app.config['API_FROM'] = os.environ.get('API_FROM')
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'

bootstrap = Bootstrap(app)
moment = Moment(app)
db.init_app(app)
migrate = Migrate(app, db)

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
                f"Novo usuário cadastrado:\n"
                f"Nome: {form.name.data}\n"
                f"Prontuário: {form.prontuario.data}\n"
                f"Usuário: {form.name.data}\n"
                f"E-mail: {form.email.data}"
            )

            # Envia e-mail para o admin e o e-mail institucional do usuário
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
                           known=session.get('known', False),
                           users=users, current_time=datetime.utcnow())

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)
