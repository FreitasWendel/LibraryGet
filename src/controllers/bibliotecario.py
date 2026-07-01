from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from datetime import datetime, timedelta

from src.controllers.auth import login_required
from src.models import db
from src.models.livro import Livro
from src.models.usuario import Usuario
from src.models.emprestimo import Emprestimo
from sqlalchemy import func

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

@bibliotecario_bp.route('/registrar-emprestimo', methods=['POST'])
@login_required('Administrador')
def registrar_emprestimo():
    usuario_id = request.form.get('usuario_id')
    livro_id = request.form.get('livro_id')
    
    livro = Livro.query.get_or_404(livro_id)
    usuario = Usuario.query.get_or_404(usuario_id)

    
    if livro.quantidade_disponivel <= 0:
        flash(f'Não há estoque disponível para o livro "{livro.titulo}".', 'danger')
        return redirect(url_for('acervo.lista_livros'))


    ja_possui = Emprestimo.query.filter_by(
        usuario_id=usuario_id, 
        livro_id=livro_id, 
        status='ATIVO'
    ).first()
    
    if ja_possui:
        flash(f'O usuário {usuario.nome} já está em posse de um exemplar ativo deste livro.', 'warning')
        return redirect(url_for('acervo.lista_livros'))

    
    limite_maximo = 5 if usuario.perfil == 'Professor' else 3
    total_ativos = Emprestimo.query.filter_by(usuario_id=usuario_id, status='ATIVO').count()
    
    if total_ativos >= limite_maximo:
        flash(f'Limite excedido! {usuario.nome} já possui {total_ativos} empréstimos ativos (Máximo permitido: {limite_maximo}).', 'danger')
        return redirect(url_for('acervo.lista_livros'))

    try:
        
        livro.quantidade_disponivel -= 1
        prazo_devolucao = datetime.utcnow() + timedelta(days=14)

        novo_emprestimo = Emprestimo(
            usuario_id=usuario_id,
            livro_id=livro_id,
            data_prevista=prazo_devolucao, 
            status='ATIVO'
        )

        db.session.add(novo_emprestimo)
        db.session.commit()
        
        flash(f'Sucesso! Empréstimo do livro "{livro.titulo}" registrado para {usuario.nome}.', 'success')
        return redirect(url_for('acervo.lista_livros'))
        
    except Exception as e:
        db.session.rollback()
        flash('Erro interno ao tentar salvar o empréstimo.', 'danger')
        return redirect(url_for('acervo.lista_livros'))
    


@bibliotecario_bp.route('/gerenciar-emprestimos')
@login_required('Administrador')
def gerenciar_emprestimos():
    
    emprestimos_ativos = Emprestimo.query.filter_by(status='ATIVO').order_by(Emprestimo.data_prevista.asc()).all()
    return render_template('bibliotecario/gerenciar_emprestimos.html', emprestimos=emprestimos_ativos, datetime=datetime)



@bibliotecario_bp.route('/devolver/<int:emprestimo_id>', methods=['POST'])
@login_required('Administrador')
def registrar_devolucao(emprestimo_id):
    emprestimo = Emprestimo.query.get_or_404(emprestimo_id)
    
    if emprestimo.status != 'ATIVO':
        flash('Este empréstimo já foi baixado ou está inválido.', 'warning')
        return redirect(url_for('bibliotecario.gerenciar_emprestimos'))

    try:
    
        emprestimo.status = 'DEVOLVIDO'
        emprestimo.data_devolucao = datetime.utcnow()
        
        
        emprestimo.livro.quantidade_disponivel += 1
        
        db.session.commit()
        flash(f'Sucesso! Devolução do livro "{emprestimo.livro.titulo}" (Leitor: {emprestimo.usuario.nome}) registrada com sucesso.', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash('Erro interno ao tentar registrar a devolução no banco de dados.', 'danger')
        
    return redirect(url_for('bibliotecario.gerenciar_emprestimos'))

@bibliotecario_bp.route('/relatorios')
@login_required('Administrador')
def relatorio_estatistico():
    try:
       
        livros_por_categoria = db.session.query(
            Livro.categoria,
            func.count(Livro.id).label('total')
        ).group_by(Livro.categoria).all()

        
        total_ativos = Emprestimo.query.filter_by(status='ATIVO').count()

       
        usuarios_atrasados = Emprestimo.query.filter(
            Emprestimo.status == 'ATIVO',
            Emprestimo.data_prevista < datetime.utcnow()
        ).order_by(Emprestimo.data_prevista.asc()).all()

        return render_template(
            'bibliotecario/relatorio.html',
            categorias=livros_por_categoria,
            total_ativos=total_ativos,
            atrasados=usuarios_atrasados,
            datetime=datetime 
        )
        
    except Exception as e:
        flash('Erro ao processar dados estatísticos do relatório.', 'danger')
        return redirect(url_for('bibliotecario.painel'))