from src.controllers.auth import auth_bp
from src.controllers.acervo import acervo_bp
from src.controllers.bibliotecario import bibliotecario_bp
from src.controllers.professor import professor_bp
from src.controllers.aluno import aluno_bp
from src.controllers.emprestimos import emprestimos_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(acervo_bp)
    app.register_blueprint(bibliotecario_bp)
    app.register_blueprint(professor_bp)
    app.register_blueprint(aluno_bp)
    app.register_blueprint(emprestimos_bp)