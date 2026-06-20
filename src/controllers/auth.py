from flask import Blueprint, render_template, request, redirect, url_for,flash,session 
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
            
            if usuario.perfil == 'admin':
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