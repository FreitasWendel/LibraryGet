from flask import Blueprint, render_template, url_for, redirect, request, flash, session
from src.models import db
from src.models.livro import Livro
from src.models.usuario import Usuario
from src.controllers.auth import login_required

acervo_bp = Blueprint('acervo', __name__, url_prefix='/acervo')

@acervo_bp.route('/')
def home():
    
    if 'usuario_perfil' in session:
        if session['usuario_perfil'] == 'Administrador':
            return redirect(url_for('bibliotecario.painel'))
        elif session['usuario_perfil'] == 'Professor':
            return redirect(url_for('professor.painel'))
        else:
            return redirect(url_for('aluno.painel'))
            
    return render_template('acervo/home.html')

@acervo_bp.route('/livros')
def lista_livros():
    livros = Livro.query.all()

    usuarios = []
    if session.get('usuario_perfil') == 'Administrador':
        usuarios = Usuario.query.filter(Usuario.perfil != 'Administrador').all()
    return render_template('acervo/lista_livros.html', livros=livros, usuarios=usuarios)

@acervo_bp.route('/livros/novo', methods=['GET', 'POST'])
@login_required('Administrador')
def novo_livro():

    if request.method == 'POST':
        try:
            livro = Livro(
                titulo=request.form['titulo'],
                autor=request.form['autor'],
                categoria=request.form['categoria'],
                isbn=request.form['isbn'],
                editora=request.form.get('editora'),
                quantidade_total=int(request.form['quantidade']),
                quantidade_disponivel=int(request.form['quantidade'])
            )

            db.session.add(livro)
            db.session.commit()
            flash('Livro cadastrado com sucesso!', 'success')
            return redirect(url_for('acervo.lista_livros'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao cadastrar livro. Verifique os dados e tente novamente.', 'danger')
            return redirect(url_for('acervo.lista_livros'))
    
    return render_template('acervo/novo_livro.html')

@acervo_bp.route('/livros/editar/<int:id>', methods=['GET', 'POST'])
@login_required('Administrador')
def editar_livro(id):
    livro = Livro.query.get_or_404(id)

    if request.method == 'POST':
        try:
            nova_qtd_total = int(request.form['quantidade'])
            
            diferenca = nova_qtd_total - livro.quantidade_total

            livro.titulo = request.form['titulo']
            livro.autor = request.form['autor']
            livro.categoria = request.form['categoria']
            livro.isbn = request.form['isbn']
            livro.editora = request.form.get('editora')
            livro.quantidade_total = int(request.form['quantidade'])
            livro.quantidade_disponivel = int(request.form['quantidade'])

            diferenca = int(request.form['quantidade']) - livro.quantidade_total
            livro.quantidade_total = int(request.form['quantidade'])
            livro.quantidade_disponivel += diferenca

            db.session.commit()
            flash('Livro atualizado com sucesso!', 'success')

            return redirect(url_for('acervo.lista_livros'))
        
        except Exception as e:
            db.session.rollback()
            flash('Erro ao atualizar livro.', 'error')
            return redirect(url_for('acervo.lista_livros'))

    return render_template('acervo/editar_livro.html', livro=livro)

@acervo_bp.route('/livros/deletar/<int:id>', methods=['POST'])
@login_required('Administrador')
def deletar_livro(id):
    livro = Livro.query.get_or_404(id)
    try:
        db.session.delete(livro)
        db.session.commit()
        flash('Livro removido do acervo.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Não é possível remover este livro (pode haver empréstimos ativos).', 'danger')
        
    return redirect(url_for('acervo.lista_livros'))