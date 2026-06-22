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