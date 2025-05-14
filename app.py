from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, jsonify
from functools import wraps
import logging
import json
import os
import sys

# Modifique a configuração do logger para:
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logger.log'),  # Arquivo local
        logging.StreamHandler(sys.stdout)   # Saída para o Render
    ]
)

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
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Login</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }
                .login-container {
                    background: white;
                    padding: 2rem;
                    border-radius: 8px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    width: 300px;
                    text-align: center;
                }
                .login-container h2 {
                    margin-bottom: 1.5rem;
                    color: #333;
                }
                .login-container input {
                    width: 100%;
                    padding: 0.75rem;
                    margin: 0.5rem 0;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    box-sizing: border-box;
                }
                .login-container button {
                  width: 100%;
                   padding: 0.75rem;
                  background-color: #e73d3d;  /* Novo vermelho */
                 color: white;
                   border: none;
                   border-radius: 4px;
                 cursor: pointer;
                 font-size: 1rem;
                  margin-top: 1rem;
}
                .login-container button:hover {
                   background-color: #c53131;  /* Vermelho mais escuro para o hover */
                 }                   
                .error-message {
                    color: #dc3545;
                    margin-top: 1rem;
                }
            </style>
        </head>
        <body>
            <div class="login-container">
                <h2>Login</h2>
                <form method="post">
                    <input name="username" placeholder="Usuário" required><br>
                    <input name="password" type="password" placeholder="Senha" required><br>
                    <button type="submit">Entrar</button>
                </form>
                <div class="error-message">Usuário ou senha inválidos</div>
            </div>
        </body>
        </html>
        '''
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .login-container {
                background: white;
                padding: 2rem;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                width: 300px;
                text-align: center;
            }
            .login-container h2 {
                margin-bottom: 1.5rem;
                color: #333;
            }
            .login-container input {
                width: 100%;
                padding: 0.75rem;
                margin: 0.5rem 0;
                border: 1px solid #ddd;
                border-radius: 4px;
                box-sizing: border-box;
            }
            .login-container button {
                width: 100%;
                padding: 0.75rem;
                background-color: #e73d3d;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 1rem;
                margin-top: 1rem;
            }
            .login-container button:hover {
                background-color: #c53131;
            }
        </style>
    </head>
    <body>
        <div class="login-container">
            <h2>Login</h2>
            <form method="post">
                <input name="username" placeholder="Usuário" required><br>
                <input name="password" type="password" placeholder="Senha" required><br>
                <button type="submit">Entrar</button>
            </form>
        </div>
    </body>
    </html>
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