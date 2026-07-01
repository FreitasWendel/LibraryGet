from src.models import db

class Livro(db.Model):
    __tablename__ = 'livros'

    id = db.Column(db.Integer, primary_key=True)

    titulo = db.Column(db.String(200), nullable=False)

    autor = db.Column(db.String(200), nullable=False)

    categoria = db.Column(db.String(100), nullable=False)

    editora = db.Column(db.String(100), nullable=True)

    ano = db.Column(db.Integer)

    isbn = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    quantidade_total = db.Column(
        db.Integer,
        nullable=False,
        default=1
    )

    quantidade_disponivel = db.Column(
        db.Integer,
        nullable=False,
        default=1
    )