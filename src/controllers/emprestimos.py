from flask import Blueprint, render_template
from src.controllers.auth import login_required

emprestimos_bp = Blueprint(
    'emprestimos',
    __name__,
    url_prefix='/emprestimos'
)

@emprestimos_bp.route('/')
@login_required('Administrador')
def listar():
    return render_template('emprestimos/lista.html')
