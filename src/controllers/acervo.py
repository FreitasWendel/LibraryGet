from flask import Blueprint, render_template, url_for, redirect, request, flash
from src.models import db
from src.models.livro import Livro

acervo_bp = Blueprint('acervo', __name__, url_prefix='/acervo')


@acervo_bp.route('/livros')
def lista_livros():
    livros = Livro.query.all()
    return render_template('acervo/lista_livros.html', livros=livros)

@acervo_bp.route('/livros/novo', methods=['GET', 'POST'])

def novo_livro():

    if request.method == 'POST':

        livro = Livro(
            titulo=request.form['titulo'],
            autor=request.form['autor'],
            categoria=request.form['categoria'],
            isbn=request.form['isbn'],
            quantidade_total=int(request.form['quantidade']),
            quantidade_disponivel=int(request.form['quantidade'])
        )

        db.session.add(livro)
        db.session.commit()

        return redirect(url_for('acervo.lista_livros'))

    return render_template('acervo/novo_livro.html')

@acervo_bp.route('/livros/editar/<int:id>', methods=['GET', 'POST'])
def editar_livro(id):
    livro = Livro.query.get_or_404(id)

    if request.method == 'POST':
        try:
            
            livro.titulo = request.form['titulo']
            livro.autor = request.form['autor']
            livro.categoria = request.form['categoria']
            livro.isbn = request.form['isbn']
            livro.quantidade_total = int(request.form['quantidade'])
            livro.quantidade_disponivel = int(request.form['quantidade'])

            diferenca = int(request.form['quantidade']) - livro.quantidade_total
            livro.quantidade_total = int(request.form['quantidade'])
            livro.quantidade_disponivel += diferenca

            db.session.commit()
            flash('Livro atualizado com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Erro ao atualizar livro.', 'error')

    return render_template('acervo/editar_livro.html', livro=livro)

@acervo_bp.route('/livros/deletar/<int:id>', methods=['POST'])
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