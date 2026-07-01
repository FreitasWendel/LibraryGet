from src.models import db
from datetime import datetime

class SugestaoLivro(db.Model):
    __tablename__ = 'sugestoes_livros'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(150), nullable=False)
    justificativa = db.Column(db.Text, nullable=False)
    data_sugestao = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='PENDENTE')
    
    
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    professor = db.relationship('Usuario', backref='sugestoes_do_professor')