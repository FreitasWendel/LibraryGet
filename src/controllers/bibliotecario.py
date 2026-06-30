from flask import Blueprint, render_template
from datetime import datetime

from src.controllers.auth import login_required
from src.models.livro import Livro
from src.models.emprestimo import Emprestimo

bibliotecario_bp = Blueprint(
    'bibliotecario',
    __name__,
    url_prefix='/admin'
)

@bibliotecario_bp.route('/painel')
@login_required('Administrador')
def painel():

    total_livros = Livro.query.count()

    emprestimos_ativos = Emprestimo.query.filter_by(
        status='ATIVO'
    ).count()

    alertas_atraso = Emprestimo.query.filter(
        Emprestimo.status == 'ATIVO',
        Emprestimo.data_prevista < datetime.now()
    ).count()

    dados_painel = {
        'total_livros': total_livros,
        'emprestimos_ativos': emprestimos_ativos,
        'alertas_atraso': alertas_atraso
    }

    return render_template(
        'bibliotecario/painel.html',
        dados=dados_painel
    )