from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Para usar o flash

def init_db():
    conn = sqlite3.connect('inquilinos.db')
    
    
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS inquilinos (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            password TEXT,
            telefone TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

@app.route('/', methods=['GET'])
def home():
    return render_template("cadastro.html")

@app.route('/inquilinos', methods=['POST'])
def add_user():
    novo_inquilino = request.form  # Mudei para receber dados do formulário
    conn = sqlite3.connect('inquilinos.db')
    c = conn.cursor()
    c.execute('INSERT INTO inquilinos (name, email, password, telefone) VALUES (?, ?, ?, ?)', 
              (novo_inquilino['name'], novo_inquilino['email'], novo_inquilino['password'], novo_inquilino['telefone']))
    conn.commit()
    conn.close()
    flash('Cadastro realizado com sucesso!', 'success')  # Mensagem de sucesso
    return redirect(url_for('login'))  # Redireciona para a página de login

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        dados_login = request.form
        conn = sqlite3.connect('inquilinos.db')
        c = conn.cursor()
        c.execute('SELECT * FROM inquilinos WHERE email = ? AND password = ?', 
                  (dados_login['email'], dados_login['password']))
        usuario = c.fetchone()
        conn.close()
        
        if usuario:
            flash('Bem Vindo(a)!', 'success')
            return redirect(url_for('listar_anuncios'))  # Redireciona para a página de listagem de anuncios
        else:
            flash('Credenciais inválidas!', 'error')
            return redirect(url_for('login'))  # Redireciona para o formulário de login
    else:
        return render_template("login.html")
    
@app.route('/anuncios', methods=['GET'])
def listar_anuncios():
    conn = sqlite3.connect('ihouse.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM imoveis')  # Buscando todos os anúncios
    anuncios = c.fetchall()
    
    conn.close()
    
    return render_template("anuncios.html", anuncios=anuncios)  # Passando os anúncios para o template


@app.route('/solicitar_aluguel', methods=['POST'])
def solicitar_aluguel():
    dados_solicitacao = request.form  # Recebendo dados do formulário
    anuncio_id = dados_solicitacao.get('anuncio_id')
    inquilino_id = dados_solicitacao.get('inquilino_id')
    
    if not anuncio_id or not inquilino_id:
        flash('Erro: Anúncio ou Inquilino não especificados!', 'danger')
        return redirect(url_for('home'))
    
    try:
        conn = sqlite3.connect('aluguel.db')
        c = conn.cursor()
        c.execute('INSERT INTO aluguel(anuncio_id, inquilino_id) VALUES (?, ?)', 
                  (anuncio_id, inquilino_id))
        conn.commit()
        flash('Solicitação de aluguel realizada!', 'success')  # Mensagem de sucesso
    except Exception as e:
        flash(f'Erro ao realizar a solicitação: {str(e)}', 'danger')  # Mensagem de erro
    finally:
        conn.close()
    
    return redirect(url_for('home'))  # Redireciona para a página inicial


if __name__ == '__main__':
    init_db()
    app.run(port=5001)
