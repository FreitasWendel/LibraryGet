from datetime import datetime, timedelta
from src.models import db

class Emprestimo(db.Model):
    __tablename__ = 'emprestimos'

    id = db.Column(db.Integer, primary_key=True)

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id'),
        nullable=False
    )

    livro_id = db.Column(
        db.Integer,
        db.ForeignKey('livros.id'),
        nullable=False
    )

    data_emprestimo = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    data_prevista = db.Column(
        db.DateTime,
        nullable=False
    )

    data_devolucao = db.Column(
        db.DateTime,
        nullable=True
    )

    status = db.Column(
        db.String(20),
        default='ATIVO'
    )

    usuario = db.relationship('Usuario')
    livro = db.relationship('Livro')