from flask import Flask
from flasgger import Swagger
#import os
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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização do banco SQLite
db.init_app(app)

# Importação de rotas
from routes import professores, turmas
app.register_blueprint(professores.appProfessor)
app.register_blueprint(turmas.appTurma)

# Criação das tabelas
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=False, port=5000)
    # port = int(os.environ.get('PORT', 5000)) 
    # debug_mode = os.environ.get('FLASK_ENV', 'production') == 'development'
