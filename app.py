import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_login import LoginManager, login_manager, current_user, login_required, login_user, logout_user
from flask import Flask, render_template, flash, redirect, url_for, request
from forms.forms import FormularioRegistro, FormularioLogin, FormularioPet, RegistroServicoUm
from helpers.database import migrate, db

from models.user import User
from models.pet import Pet
from models.passeioparque import PasseioParque

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://marcella:409014@localhost:5432/petconfy-services"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

login_manager = LoginManager(app)
login_manager.init_app(app)
db.init_app(app)
migrate.init_app(app, db)


@app.before_first_request
def create_database():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/home')
def home():
    return render_template('user.html')

@app.route('/admin')
@login_required
def admin():
    user_id = current_user.id
    if current_user.is_authenticated and user_id == 1:
        users = User.query.all()
        return render_template('adm.html', users=users)
    else:
        return render_template('forbidden.html')

@app.route('/admin/search', methods=['GET'])
@login_required
def procurar():
    user_id = current_user.id
    if current_user.is_authenticated and user_id == 1:
        nome = request.args.get('nome')
        if nome is not None:
            users = User.query.filter(User.nome.like(f"%{nome}%")).all()
        else:
            users = User.query.all()
        return render_template('adm.html', users=users)
    else:
        return render_template('forbidden.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = FormularioRegistro()
    if form.validate_on_submit():
        user = User(nome=form.nome.data, email=form.email.data,
                    endereco=form.endereco.data, senha_hash=form.senha1.data)
        user.set_senha(form.senha1.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = FormularioLogin()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_senha(form.senha.data):
            login_user(user)
            proximo = request.args.get("proximo")
            return redirect(proximo or url_for('home'))
        flash('Endereço de email e/ou senha inválidos.')
    return render_template('login.html', form=form)


@app.route("/forbidden", methods=['GET', 'POST'])
@login_required
def protected():
    return redirect(url_for('forbidden.html'))


@app.route("/logout")
# @login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/pet', methods=['GET', 'POST'])
def cadastroPet():
    form = FormularioPet()
    if form.validate_on_submit():
        user_id = current_user.id
        user = User.query.get(user_id)
        pet = Pet(nome=form.nomePet.data, idade=form.idade.data,
                  especie=form.especie.data, observacoes=form.observacoes.data, user=user)
        db.session.add(pet)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('cadastropet.html', form=form)


@app.route('/pets', methods=['GET'])
@login_required
def getPet():
    if current_user.is_authenticated:
        user_id = current_user.id
        # Listar os pets do usuário logado
        pets = Pet.query.filter_by(user_id=user_id).all()
        return render_template('pets.html', pets=pets)


@app.route('/pets/<int:id>', methods=['GET', 'DELETE'])
@login_required
def deletePet(id):
    if current_user.is_authenticated:
        user_id = current_user.id
        print(user_id)
        #pets = Pet.query.filter_by(user_id=user_id).all()
        pet = Pet.query.get(id)
        if pet is not None:
            db.session.delete(pet)
            db.session.commit()
            pets = Pet.query.filter_by(user_id=user_id).all()
            return render_template('pets.html', pets=pets)
        else:
            return 'PET NÃO ENCONTRADO'
    else:
        return 'SEM AUTORIZAÇÃO', 405


@app.route('/pets/<int:id>', methods=['GET', 'POST'])
@login_required
def updatePet(id):
    if current_user.is_authenticated:
        user_id = current_user.id
    else:
        return None
    pet = Pet.query.get(id)
    if not pet:
        flash('PET NÃO ENCONTRADO', 'error')
        return redirect(url_for('pets'))

    if pet.user_id != user_id:
        flash('PERMISSÃO NEGADA', 'error')
        return redirect(url_for('pets'))

    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        especie = request.form['especie']
        observacoes = request.form['observacoes']
        pet.nome = nome
        pet.idade = idade
        pet.especie = especie
        pet.observacoes = observacoes
        db.session.commit()

    pets = Pet.query.filter_by(user_id=user_id).all()
    return render_template('pets.html', pets=pets)


@app.route('/passeioparque', methods=['POST', 'GET'])
@login_required
def passeioparque():
    form = RegistroServicoUm()
    if form.validate_on_submit():
        user_id = current_user.id
        user = User.query.get(user_id)
        passeioparque = PasseioParque(data_inicial=form.data_inicial.data, data_final=form.data_final.data,
                    hora_inicial=form.hora_inicial.data, hora_final=form.hora_final.data, telefone=form.telefone.data, user=user)
        db.session.add(passeioparque)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('servicoum.html', form=form)

@app.route('/perfil', methods=['GET'])
@login_required
def perfil():
    if current_user.is_authenticated:
        user_id = current_user.id
        # Listar os pets do usuário logado
        perfil = PasseioParque.query.filter_by(user_id=user_id).all()
        return render_template('perfil.html', perfil=perfil)


@app.route('/agenda')
@login_required
def agenda():
    return render_template('agenda.html')

if __name__ == "__main__":
    app.run(debug=True)