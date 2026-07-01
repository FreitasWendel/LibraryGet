from flask import Blueprint, render_template, redirect, url_for, flash, session
from datetime import datetime, timedelta
from src.models import db
from src.models.livro import Livro
from src.models.emprestimo import Emprestimo
from src.controllers.auth import login_required

professor_bp = Blueprint('professor', __name__, url_prefix='/professor')


@professor_bp.route('/painel')
@login_required('Professor')
def painel():
    usuario_id = session.get('usuario_id')
    
    
    livros_emprestados = Emprestimo.query.filter_by(usuario_id=usuario_id, status='ATIVO').count()
    historico_total = Emprestimo.query.filter_by(usuario_id=usuario_id).count()
    
    dados_professor = {
        'livros_emprestados': livros_emprestados,
        'historico_total': historico_total
    }
    return render_template('professor/painel.html', dados=dados_professor)



@professor_bp.route('/solicitar-emprestimo/<int:livro_id>', methods=['POST'])
@login_required('Professor')
def solicitar_emprestimo(livro_id):
    usuario_id = session.get('usuario_id')
    livro = Livro.query.get_or_404(livro_id)

    
    if livro.quantidade_disponivel <= 0:
        flash(f'Desculpe, o livro "{livro.titulo}" está esgotado no momento.', 'danger')
        return redirect(url_for('acervo.lista_livros'))

    
    ja_possui = Emprestimo.query.filter_by(
        usuario_id=usuario_id, 
        livro_id=livro_id, 
        status='ATIVO'
    ).first()
    
    if ja_possui:
        flash(f'Você já possui um empréstimo ativo do livro "{livro.titulo}".', 'warning')
        return redirect(url_for('acervo.lista_livros'))

    try:
        livro.quantidade_disponivel -= 1
        
        
        prazo_devolucao = datetime.utcnow() + timedelta(days=15) 

        novo_emprestimo = Emprestimo(
            usuario_id=usuario_id,
            livro_id=livro_id,
            data_prevista=prazo_devolucao, 
            status='ATIVO'
        )

        db.session.add(novo_emprestimo)
        db.session.commit()
        
        data_formatada = prazo_devolucao.strftime('%d/%m/%Y')
        flash(f'Sucesso! O livro "{livro.titulo}" foi reservado para o docente. Retire na biblioteca. Devolução até: {data_formatada}.', 'success')
        
        return redirect(url_for('professor.painel'))
        
    except Exception as e:
        db.session.rollback()
        flash('Erro ao processar o pedido de empréstimo do professor.', 'danger')
        return redirect(url_for('acervo.lista_livros'))
    
@professor_bp.route('/historico')
@login_required('Professor')
def historico_professor():
    usuario_id = session.get('usuario_id')
    meus_emprestimos = Emprestimo.query.filter_by(usuario_id=usuario_id).order_by(Emprestimo.data_emprestimo.desc()).all()
    
    return render_template('emprestimo/relatorio.html', emprestimos=meus_emprestimos)