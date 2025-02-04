from flask import Flask, request, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import secrets


app = Flask(__name__)


app.config['SECRET_KEY'] = secrets.token_hex(8)
#O ENDEREÇO DO BANCO
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://deployApiDB_chosenmove:7ab603edd69d6ff610c42e6579f19dfb4f0280a9@2zrxo.h.filess.io:5433/deployApiDB_chosenmove?options=-csearch_path%3Ddbo,public,meu_schema'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#CONECTO O BANCO A APLICAÇÃO
db = SQLAlchemy(app)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    senha_hash = db.Column(db.String(200), nullable=False) 

    # Método para definir a senha de forma segura (cripto)
    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    # Método para verificar a senha fornecida com o hash armazenado
    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def __repr__(self):
        return f'<Usuario {self.nome}>'



@app.get('/')
def index():
    return 'Olá! Estou funcionando.'


@app.route('/criar_usuario', methods=['POST','GET'])
def criar_usuario():
    if request.method == 'POST':
        
        nome = request.form.get('nome')
        senha = request.form.get('senha')
        
        if not nome or not senha:
            return "Nome e senha são obrigatórios", 400
        
        novo_usuario = Usuario(nome=nome)
        novo_usuario.set_senha(senha)  # Criptografa a senha
        
        db.session.add(novo_usuario)
        db.session.commit()
        
        return "Usuário criado com sucesso!", 201
    else:
        return render_template('cadastro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        # Verificar se os campos estão preenchidos
        if not nome or not senha:
            flash('Nome e senha são obrigatórios!', 'error')
            return redirect(url_for('login'))

        # Buscar o usuário no banco de dados
        usuario = Usuario.query.filter_by(nome=nome).first()

        # Verificar se o usuário existe e a senha está correta
        if usuario and usuario.verificar_senha(senha):
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('home'))  # Roteamento para uma página inicial (home)
        else:
            flash('Credenciais inválidas', 'error')
            return redirect(url_for('login'))

    # Se o método for GET, exibe o formulário de login
    return render_template('login.html')





if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()

