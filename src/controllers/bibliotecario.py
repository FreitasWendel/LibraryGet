from flask import Blueprint, render_template
from src.controllers.auth import login_required

bibliotecario_bp = Blueprint('bibliotecario', __name__, url_prefix='/admin')

@bibliotecario_bp.route('/painel')
@login_required('Administrador')
def painel():

    dados_painel = {
        'total_livros': 120,
        'emprestimos_ativos': 15,
        'alertas_atraso': 3
    }

    return render_template('bibliotecario/painel.html', dados=dados_painel)