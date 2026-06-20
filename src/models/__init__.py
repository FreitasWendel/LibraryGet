from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()   

from src.models.usuario import Usuario
from src.models.livro import Livro
from src.models.emprestimo import Emprestimo