from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# 1. SECRET KEY DINÂMICA
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or '6236128622fa7e7b571e02cf4f96256e'

# 2. BANCO DE DADOS INTELIGENTE (Supabase vs Local)
# ... imports ...

database_url = os.environ.get('DATABASE_URL')

# --- INÍCIO DO CÓDIGO DE DEBUG ---
print("--- DEBUG DO BANCO DE DADOS ---")
if database_url:
    # Mostra só os 10 primeiros caracteres para não vazar a senha no log
    print(f"URL ENCONTRADA: {database_url[:15]}...")
else:
    print("URL NÃO ENCONTRADA! O SITE VAI TENTAR USAR SQLITE E VAI FALHAR.")
print("-----------------------------")
# --- FIM DO CÓDIGO DE DEBUG ---


# ... resto do código ...

# Corrige o problema do 'postgres://' que alguns sistemas usam
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), "users.db")

bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)
db = SQLAlchemy(app)

# Importa os modelos para o banco conhecer as tabelas
from .models import User
from Program import forms
from Program import routes

# 3. CRIAÇÃO AUTOMÁTICA DAS TABELAS (Substitui o init_db.py)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)