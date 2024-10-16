from flask import Flask, render_template, request, redirect, url_for, jsonify, g, session,flash
import sqlite3

app = Flask(__name__)
DATABASE = 'ihouse.db'
app.secret_key = 'ADin!23'  # Defina uma chave secreta única

# Função para conectar ao banco de dados
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Fechar a conexão com o banco de dados quando a aplicação terminar
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Inicializar o banco de dados
def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS proprietarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                telefone TEXT NOT NULL,
                senha TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS imoveis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                comodos INTEGER NOT NULL,
                valor REAL NOT NULL,
                localizacao TEXT NOT NULL,
                proprietario_id INTEGER NOT NULL,
                FOREIGN KEY (proprietario_id) REFERENCES proprietarios(id)
            )
        ''')
        db.commit()

# Chame init_db() uma vez para criar as tabelas
#init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/painel/<int:id>')
def painel(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM imoveis WHERE proprietario_id = ?', (id,))
    imoveis = cursor.fetchall()

    imoveis_lista = []
    for imovel in imoveis:
        imoveis_lista.append({
            'tipo': imovel[1],
            'comodos': imovel[2],
            'valor': imovel[3],
            'localizacao': imovel[4]
        })
    
    return render_template('painel.html', imoveis=imoveis_lista)

# Cadastro de proprietários
@app.route('/proprietarios/cadastrar', methods=['POST'])
def cadastrar_proprietario():
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    senha = request.form['senha']

    db = get_db()
    cursor = db.cursor()
    
    # Verificar se o email já existe
    cursor.execute('SELECT * FROM proprietarios WHERE email = ?', (email,))
    if cursor.fetchone() is not None:
        return "Email já cadastrado!"
    
    cursor.execute('''
        INSERT INTO proprietarios (nome, email, telefone, senha) 
        VALUES (?, ?, ?, ?)
    ''', (nome, email, telefone, senha))
    
    db.commit()
    
    return redirect(url_for('login'))

# Login de proprietários
@app.route('/proprietarios/login', methods=['POST'])
def login_proprietario():
    email = request.form['email']
    senha = request.form['senha']

    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM proprietarios WHERE email = ? AND senha = ?', (email, senha))
    proprietario = cursor.fetchone()


    if proprietario:
        session['id'] = proprietario[0]  # Armazena o ID do proprietário na sessão
        flash('Bem Vindo(a)!', 'success')
        return redirect(url_for('painel',id=session['id']))
    else:
        flash('Credenciais inválidas!', 'error')
        return redirect(url_for('login'))

    # if proprietario:
    #     return redirect(url_for('painel', proprietario_id=proprietario[0]))
    # else:
    #     return "Credenciais inválidas!"

# Cadastrar imóveis
@app.route('/imoveis', methods=['POST'])
def criar_imovel():
    tipo = request.form['tipo']
    comodos = request.form['comodos']
    valor = request.form['valor']
    localizacao = request.form['localizacao']
    

    # Obtém o proprietario_id da sessão
    proprietario_id = session.get('id')

    if not proprietario_id:
        flash('Você precisa estar logado para criar um imóvel!', 'danger')
        return redirect(url_for('login'))

    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO imoveis (tipo, comodos, valor, localizacao, proprietario_id)
        VALUES (?, ?, ?, ?, ?)
    ''', (tipo, comodos, valor, localizacao, proprietario_id))
    
    db.commit()
    
    return redirect(url_for('painel', id=proprietario_id))

if __name__ == '__main__':
    app.run(debug=True)
