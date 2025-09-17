from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
    nome = StringField('Informe o seu nome', validators=[DataRequired()])
    sobrenome = StringField('Informe o seu sobrenome', validators=[DataRequired()])
    instituicao = StringField('Informe a sua Instituição de ensino', validators=[DataRequired()])
    disciplina = SelectField('Informe a sua disciplina',
                             choices=[('DSWA5', 'DSWA5'),
                                      ('DWBA4', 'DWBA4'),
                                      ('Gestão de Projetos', 'Gestão de Projetos')],
                             validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', 
                           form=form, 
                           name=session.get('name'), 
                           current_time=datetime.utcnow())

@app.route("/user")
def user():
    return render_template("user.html")

@app.route("/contexto")
def contexto():
    return render_template('contexto.html')

@app.errorhandler(404)
def notfound(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internalerror(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(debug=True)
