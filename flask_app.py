from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route("/")
def home():
    return render_template('index.html', current_time=datetime.utcnow())

@app.route("/user")
def user():
    return render_template("user.html")

@app.errorhandler(404)
def notfound(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internalerror(e):
    return render_template('500.html'), 500

# @app.route("/contexto")
# def contexto():
#     return render_template("contexto.html")

if __name__ == "__main__":
    app.run(debug=True)
