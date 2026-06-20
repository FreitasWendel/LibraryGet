from src.controllers.auth import auth_bp
from src.controllers.acervo import acervo_bp
def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(acervo_bp)