from flask import Blueprint, render_template, request, redirect, url_for, flash, session 
from src.models.usuario import Usuario
import functools
from functools import wraps
from src.models import db
from src.models.usuario import Usuario

auth_bp = Blueprint('auth', __name__)

def login_obrigatorio_perfil(perfil_exigido):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'usuario_id' not in session:
                flash('Faça login para acessar esta página.', 'warning')
                return redirect(url_for('auth.login'))
            if session.get('usuario_perfil') != perfil_exigido:
                flash('Você não tem permissão para acessar esta página.', 'danger')
                return redirect(url_for('acervo.lista_livros'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

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
    return redirect(url_for('auth.login'))

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



@auth_bp.route('/admin/cadastrar-usuario', methods=['GET', 'POST'])
@login_obrigatorio_perfil('Administrador') 
def admin_cadastro_usuario():
    if request.method == 'POST':
        nome = request.form.get('nome').strip()
        email = request.form.get('email').strip().lower()
        senha = request.form.get('senha')
        perfil_escolhido = request.form.get('perfil') 

        
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash('Este e-mail já está cadastrado.', 'danger')
            return redirect(url_for('auth.admin_cadastro_usuario'))

       
        novo_usuario = Usuario(nome=nome, email=email, perfil=perfil_escolhido)
        novo_usuario.set_senha(senha)

        try:
            db.session.add(novo_usuario)
            db.session.commit()
            flash(f'Usuário {nome} cadastrado com sucesso como {perfil_escolhido}!', 'success')
            return redirect(url_for('acervo.lista_livros'))
        except Exception as e:  
            db.session.rollback()
            flash('Erro ao salvar usuário no banco.', 'danger')
            
    return render_template('auth/admin_cadastro.html')


@auth_bp.route('/painel_redirecionar')
def redirecionar_painel():
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))
    
    perfil = session.get('usuario_perfil')

    if perfil == 'Administrador':
        return redirect(url_for('bibliotecario.painel'))
    elif perfil == 'Professor':
        return redirect(url_for('professor.painel'))
    elif perfil == 'Aluno':
        return redirect(url_for('aluno.painel'))