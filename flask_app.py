from flask import Flask, request, make_response, redirect, abort;
app = Flask(__name__);

@app.route('/')
def index():
    
    html_texto = '<h1>Avaliação contínua: Aula 030</h1>';    
    html_texto += '<ul>';    
    html_texto += '<li><a href="/">Home</a>';
    html_texto += '<li><a href="/user/Fabio Teixeira/PT23820X/IFSP">Identificação</a>';
    html_texto += '<li><a href="/contextorequisicao">Contexto da requisição</a>';
    html_texto += '</ul>';
    
    return html_texto;

@app.route('/user/<name>/<prontuario>/<institution>')
def user(name, prontuario, institution):
    html_texto = '<h1>Avaliação contínua: Aula 030</h1>';    
    html_texto += '<h2>Aluno: {}</h2>'.format(name);
    html_texto += '<h2>Prontuário: {}</h2>'.format(prontuario);
    html_texto += '<h2>Instituição: {}</h2>'.format(institution);
    html_texto += '<p><a href="/">Voltar</a></p>';

    return html_texto;

@app.route('/contextorequisicao')
def contextorequisicao():
    user_agent = request.headers.get('User-Agent');
    html_texto = '<h1>Avaliação contínua: Aula 030</h1>';    
    html_texto += '<h2>Seu navegador é: {}</h2>'.format(user_agent);
    html_texto += '<h2>O IP do cumputador remoto é: {}</h2>'.format(request.remote_addr);
    html_texto += '<h2>O host da aplicação é: {}</h2>'.format(request.host);
    html_texto += '<p><a href="/">Voltar</a></p>';

    return html_texto;