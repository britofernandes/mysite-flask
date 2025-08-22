from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/identificacao")
def identificacao():
    return render_template("identificacao.html")

@app.route("/contexto")
def contexto():
    return render_template("contexto.html")

if __name__ == "__main__":
    app.run(debug=True)
