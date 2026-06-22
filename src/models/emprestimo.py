from src.models import db

class Emprestimo(db.Model):
    __tablename__ = 'emprestimos'
    id = db.Column(db.Integer, primary_key=True)