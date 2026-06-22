from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .usuario import Usuario
from src.models.livro import Livro
from .emprestimo import Emprestimo
