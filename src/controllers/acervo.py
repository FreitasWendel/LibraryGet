from flask import Blueprint, render_template, url_for, redirect

acervo_bp = Blueprint('acervo', __name__)

@acervo_bp.route('/')
def index():
    return redirect(url_for('auth.login'))
@acervo_bp.route('/livros')
def lista_livros():

    return "<h1>Lista de Livros</h1>"