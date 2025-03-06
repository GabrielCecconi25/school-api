# app.py
from flask import Flask
from flasgger import Swagger
import os
from database import db

# Inicializa o Flask
app = Flask(__name__)

# Configuração do Swagger
app.config['SWAGGER'] = {
    'title': 'API Escola',
    'uiversion': 3
}
swagger = Swagger(app)

# Configurações do banco SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')

# Inicialização do banco SQLite
db.init_app(app)

# Importação de rotas
from routes.professores import appProfessor
app.register_blueprint(appProfessor)

# Criação das tabelas
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=False, port=5000)
