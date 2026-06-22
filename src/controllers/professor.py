from flask import Blueprint, render_template
from src.controllers.auth import login_required

professor_bp = Blueprint('professor', __name__, url_prefix='/professor')

@professor_bp.route('/painel')
@login_required('Professor')
def painel():
    dados_professor = {
        'livros_retidos': 4,
        'artigos_reservados': 1,
        'prazo_especial': True
    }
    return render_template('professor/painel.html', dados=dados_professor)