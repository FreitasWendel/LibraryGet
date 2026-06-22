from src.models import db

class Livro(db.Model):
    __tablename__ = 'livros'

    id = db.Column(db.Integer, primary_key=True)

    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(150), nullable=False)

    isbn = db.Column(db.String(20), unique=True, nullable=False)

    categoria = db.Column(db.String(100), nullable=True)

    quantidade_total = db.Column(db.Integer, default=1)
    quantidade_disponivel = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f"<Livro {self.titulo}>"