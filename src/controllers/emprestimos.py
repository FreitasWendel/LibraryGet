from flask import Blueprint, render_template, redirect, url_for, flash, request
from datetime import datetime, timedelta
from src.models import db
from src.models.emprestimo import Emprestimo
from src.models.livro import Livro
from src.models.usuario import Usuario
from src.controllers.auth import login_obrigatorio_perfil

emprestimo_bp = Blueprint('emprestimo', __name__, url_prefix='/emprestimos')


@emprestimo_bp.route('/')
@login_obrigatorio_perfil('Administrador')
def listar_emprestimos():
    emprestimos = Emprestimo.query.order_by(Emprestimo.data_emprestimo.desc()).all()
    return render_template('emprestimo/lista_emprestimos.html', emprestimos=emprestimos)


@emprestimo_bp.route('/novo', methods=['GET', 'POST'])
@login_obrigatorio_perfil('Administrador')
def novo_emprestimo():
    if request.method == 'POST':
        usuario_id = request.form.get('usuario_id')
        livro_id = request.form.get('livro_id')
        
        livro = Livro.query.get_or_404(livro_id)
        
        if livro.quantidade_disponivel <= 0:
            flash(f'Não há exemplares disponíveis do livro "{livro.titulo}".', 'danger')
            return redirect(url_for('emprestimo.novo_emprestimo'))
            
        try:
            livro.quantidade_disponivel -= 1
            
            
            novo_emp = Emprestimo(
                usuario_id=usuario_id,
                livro_id=livro_id,
                data_prevista=datetime.utcnow() + timedelta(days=14),
                status='ATIVO'
            )
            
            db.session.add(novo_emp)
            db.session.commit()
            
            flash('Empréstimo registrado com sucesso!', 'success')
            return redirect(url_for('emprestimo.listar_emprestimos'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao registrar empréstimo.', 'danger')

    usuarios = Usuario.query.filter(Usuario.perfil != 'Administrador').all()
    livros = Livro.query.filter(Livro.quantidade_disponivel > 0).all()
    return render_template('emprestimo/novo_emprestimo.html', usuarios=usuarios, livros=livros)

@emprestimo_bp.route('/devolver/<int:id>', methods=['POST'])
@login_obrigatorio_perfil('Administrador')
def devolver_livro(id):
    emprestimo = Emprestimo.query.get_or_404(id)
    
    if emprestimo.status == 'DEVOLVIDO':
        flash('Este empréstimo já foi encerrado.', 'warning')
        return redirect(url_for('emprestimo.listar_emprestimos'))
        
    try:
        emprestimo.status = 'DEVOLVIDO'
        emprestimo.data_devolucao = datetime.utcnow()
        emprestimo.livro.quantidade_disponivel += 1
        
        db.session.commit()
        flash(f'Livro "{emprestimo.livro.titulo}" devolvido com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erro ao registrar a devolução.', 'danger')
        
    return redirect(url_for('emprestimo.listar_emprestimos'))