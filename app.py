from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, jsonify
from functools import wraps
import logging
import json
import os

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

# Configurar logger
logging.basicConfig(filename='logger.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Usuários de exemplo
USERS = {
    "Allianz": "Allianz.Car10",
    "admin": "admin123"
}

# Decorador de autenticação
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['username']
        senha = request.form['password']
        if usuario in USERS and USERS[usuario] == senha:
            session['username'] = usuario
            return redirect(url_for('index'))
        return 'Usuário ou senha inválidos'
    return '''
        <form method="post">
            <input name="username" placeholder="Usuário"><br>
            <input name="password" type="password" placeholder="Senha"><br>
            <button type="submit">Entrar</button>
        </form>
    '''

# Página principal com autenticação
@app.route('/')
@login_required
def index():
    return render_template('index.html')

# Logger da busca (via JavaScript)
@app.route('/log', methods=['POST'])
@login_required
def log_search():
    data = request.get_json()
    logging.info(f"{session['username']} buscou: {data.get('endereco')}")
    return jsonify(success=True)

# Permitir download do Excel
@app.route('/vistoriadores.xlsx')
@login_required
def download_excel():
    return send_from_directory('.', 'vistoriadores.xlsx')

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)