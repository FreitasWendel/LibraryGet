from flask import Blueprint, render_template
from src.controllers.auth import login_required

aluno_bp = Blueprint('aluno', __name__, url_prefix='/aluno')

@aluno_bp.route('/painel')
@login_required('Aluno')
def painel():

    dados_aluno = {
        'livros_emprestados': 2,
        'multas_pendentes': 0.00,
        'historico_total': 8
    }
    return render_template('aluno/painel.html', dados=dados_aluno)