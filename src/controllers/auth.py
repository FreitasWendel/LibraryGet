from flask import Blueprint, render_template, request, redirect, url_for,flash,session 
from src.models.usuario import Usuario
import functools

from src.models import db
from src.models.usuario import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.check_senha(senha):
            session['usuario_id'] = usuario.id
            session['usuario_nome'] = usuario.nome
            session['usuario_perfil'] = usuario.perfil

            flash('Login realizado com sucesso!', 'success')
            
            if usuario.perfil == 'Administrador':
                return redirect(url_for('bibliotecario.painel'))
            elif usuario.perfil == 'Professor':
                return redirect(url_for('professor.painel'))
            else:
                return redirect(url_for('aluno.painel'))
            
        flash('Email ou senha incorretos. Tente novamente.', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('acervo.lista_livros'))

def login_required(perfil_exigido=None):

    def decorator(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            
            if not session.get('usuario_id'):
                flash('Faça login para acessar esta página.', 'warning')
                return redirect(url_for('auth.login'))
            
            if perfil_exigido and session.get('usuario_perfil') != perfil_exigido:
                flash('Você não tem permissão para acessar esta página.', 'danger')
                return redirect(url_for('acervo.lista_livros'))
            
            return view(**kwargs)
        return wrapped_view
    return decorator

@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome').strip()
        email = request.form.get('email').strip().lower()
        senha = request.form.get('senha')
        
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash('Email já cadastrado. Tente outro.', 'danger')
            return redirect(url_for('auth.cadastro'))

        if '@professor.' in email or email.endswith('@professor.com'):
            perfil_definido = 'Professor'
        elif '@aluno.' in email or email.endswith('@aluno.com'):
            perfil_definido = 'Aluno'
        else:
            flash('Email deve conter @professor ou @aluno para definir perfil.', 'danger')
            return redirect(url_for('auth.cadastro'))

        novo_usuario = Usuario(
            nome=nome,
            email=email,
            perfil=perfil_definido
        )       
        novo_usuario.set_senha(senha)

        try:
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Cadastro realizado com sucesso! Faça login para acessar.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao cadastrar usuário. Tente novamente.', 'danger')
            return redirect(url_for('auth.cadastro'))
        
    return render_template('auth/cadastro.html')

        