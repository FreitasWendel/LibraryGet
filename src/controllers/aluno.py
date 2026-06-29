from flask import Blueprint, render_template, redirect, url_for, flash, session
from datetime import datetime, timedelta
from src.models import db
from src.models.livro import Livro
from src.models.emprestimo import Emprestimo
from src.controllers.auth import login_required

aluno_bp = Blueprint('aluno', __name__, url_prefix='/aluno')


@aluno_bp.route('/painel')
@login_required('Aluno')
def painel():
    usuario_id = session.get('usuario_id')
    
    
    livros_emprestados = Emprestimo.query.filter_by(usuario_id=usuario_id, status='ATIVO').count()
    historico_total = Emprestimo.query.filter_by(usuario_id=usuario_id).count()
    
    dados_aluno = {
        'livros_emprestados': livros_emprestados,
        'multas_pendentes': 0.00,  
        'historico_total': historico_total
    }
    return render_template('aluno/painel.html', dados=dados_aluno)



@aluno_bp.route('/acervo')
@login_required('Aluno')
def ver_acervo():
    
    livros = Livro.query.all()
    return render_template('aluno/acervo_aluno.html', livros=livros)



@aluno_bp.route('/solicitar-emprestimo/<int:livro_id>', methods=['POST'])
@login_required('Aluno')
def solicitar_emprestimo(livro_id):
    usuario_id = session.get('usuario_id')
    livro = Livro.query.get_or_404(livro_id)

    
    if livro.quantidade_disponivel <= 0:
        flash(f'Desculpe, o livro "{livro.titulo}" está esgotado no momento.', 'danger')
        return redirect(url_for('aluno.ver_acervo'))

    
    ja_possui = Emprestimo.query.filter_by(
        usuario_id=usuario_id, 
        livro_id=livro_id, 
        status='ATIVO'
    ).first()
    
    if ja_possui:
        flash(f'Você já possui um empréstimo ativo do livro "{livro.titulo}".', 'warning')
        return redirect(url_for('aluno.ver_acervo'))

    try:
    
        livro.quantidade_disponivel -= 1

    
        novo_emprestimo = Emprestimo(
            usuario_id=usuario_id,
            livro_id=livro_id,
            data_prevista=datetime.utcnow() + timedelta(days=14), 
            status='ATIVO'
        )

        db.session.add(novo_emprestimo)
        db.session.commit()
        flash(f'Solicitação do livro "{livro.titulo}" realizada! Retire na biblioteca.', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash('Erro ao processar o seu pedido de empréstimo.', 'danger')

    return redirect(url_for('aluno.ver_acervo'))