# routes/professores.py
from flask import Blueprint, request, jsonify

from models.professor import Professor
from database import db

appProfessor = Blueprint('appProfessor', __name__)

##### GET all #####
@appProfessor.route('/professores', methods=['GET'])
def get_professores():
    """Endpoint para buscar todos os professores
    ---
    tags:
      - Professores
    responses:
      200:
        description: Lista de professores
      500:
        description: Erro de servidor
    """
    try:
      professores = Professor.query.all()
      return jsonify([professor.serialize() for professor in professores]), 200
    except Exception as e:
      db.session.rollback()
      return jsonify({'message': 'Erro de servidor', 'erro': str(e)}), 500

##### GET by ID #####
@appProfessor.route('/professores/<int:id>', methods=['GET'])
def get_professor(id):
    """Endpoint para buscar um professor por ID
    ---
    tags:
      - Professores
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do professor
    repsonses:
      200:
        description: Professor encontrado
      404:
        description: Professor não encontrado
      500:
        description: Erro de servidor
    """
    # Verificar professor
    if not db.session.query(Professor.id).filter_by(id=id).scalar():
        return jsonify({'message': 'Professor não encontrado!'}), 404

    try:
      professor = Professor.query.filter(Professor.id == id).first()
      return jsonify(professor.serialize()), 200
    except Exception as e:
      db.session.rollback()
      return jsonify({'message': 'Erro de servidor', 'erro': str(e)}), 500

##### POST #####
@appProfessor.route('/professores', methods=['POST'])
def post_professor():
    """Endpoint para cadastrar um novo professor
    ---
    tags:
      - Professores
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: "João Silva"
            idade:
              type: integer
              example: 40
            materia:
              type: string
              example: "Análise de Sistemas"
            observacoes:
              type: string
              example: "Professor especialista em desenvolvimento de software e banco de dados"
    responses:
      201:
        description: Professor criado com sucesso!
      400:
        description: Erro ao criar professor
      500:
        description: Erro de servidor
    """
    data = request.get_json()
    # Verifica se os dados foram enviados corretamente
    if not data or 'nome' not in data or 'idade' not in data or 'materia' not in data:
        return jsonify({'message': 'Dados inválidos!'}), 400
        
    # Cria um novo professor
    novo_professor = Professor(
        nome=data['nome'],
        idade=data['idade'],
        materia=data['materia'],
        observacoes=data.get('observacoes', '')
    )

    try:
      # Adiciona o professor ao banco de dados
      db.session.add(novo_professor)
      db.session.commit()
      return jsonify({'message': 'Professor criado com sucesso!'}), 201
    except Exception as e:
      db.session.rollback()
      return jsonify({'message': 'Erro de servidor', 'erro': str(e)}), 500

##### PUT #####
@appProfessor.route('/professores/<int:id>', methods=['PUT'])
def put_professor(id):
    """Endpoint para atualizar dados de um professor
    ---
    tags:
      - Professores
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do professor
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: "João Silva"
            idade:
              type: integer
              example: 45
            materia:
              type: string
              example: "Banco de Dados"
            observacoes:
              type: string
              example: "Professor atualizado com novas especialidades"
    responses:
      200:
        description: Professor atualizado
      400:
        description: Erro ao criar professor
      404:
        description: Professor não encontrado
      500:
        description: Erro de servidor
    """
    data = request.get_json()

    # Verificar dados enviados
    if not data:
      return jsonify({'message': 'Dados inválidos!'}), 400
    # Verificar professor
    if not db.session.query(Professor.id).filter_by(id=id).scalar():
      return jsonify({'message': 'Professor não encontrado!'}), 404
    
    professor = Professor.query.get(id)

    if 'nome' in data:
      professor.nome = data['nome']
    if 'idade' in data:
      professor.idade = data['idade']
    if 'materia' in data:
      professor.materia = data['materia']
    if 'observacoes' in data:
      professor.observacoes = data['observacoes']
    try:
      # Atualiza professor no banco de dados
      db.session.commit()
      return jsonify({'message': 'Professor atualizado com sucesso!'}), 200
    except Exception as e:
      db.session.rollback()
      return jsonify({'message': 'Erro de servidor', 'erro': str(e)}), 500

##### DELETE #####
@appProfessor.route('/professores/<int:id>', methods=['DELETE'])
def delete_professor(id):
    """Endpoint para deletar um professor
    ---
    tags:
      - Professores
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do professor
    responses:
      200:
        description: Professor deletado
      404:
        description: Professor não encontrado
      500:
        description: Erro de servidor
    """
    # Verificar professor
    if not db.session.query(Professor.id).filter_by(id=id).scalar():
      return jsonify({'message': 'Professor não encontrado!'}), 404
    
    try:
      db.session.delete(professor)
      db.session.commit()
      return jsonify({'message': 'Professor Deletado com sucesso!'}), 200
    except Exception as e:
      db.session.rollback()
      return jsonify({'message': 'Erro de servidor', 'erro': str(e)}), 500
