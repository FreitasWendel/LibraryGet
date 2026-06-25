from flask import Blueprint, render_template, url_for, redirect
from src.models.livro import Livro

acervo_bp = Blueprint('acervo', __name__, url_prefix='/acervo')

@acervo_bp.route('/')
def index():
    return redirect(url_for('acervo.lista_livros'))

@acervo_bp.route('/livros')
def lista_livros():
    livros = Livro.query.all()
    return render_template('acervo/lista_livros.html', livros=livros)
from flask import request
from src.models import db
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