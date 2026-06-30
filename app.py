from src import create_app
from flask import redirect, url_for, render_template

app = create_app()

@app.route('/')
def index():
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True)
@app.errorhandler(404)
def pagina_nao_encontrada(e):
    
    return render_template('erros/404.html'), 404

@app.errorhandler(403)
def acesso_proibido(e):
    return render_template('erros/403.html'), 403