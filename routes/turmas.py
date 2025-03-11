from flask import Blueprint, request, jsonify

from models.professor import Professor
from models.turma import Turma
from database import db

appTurma = Blueprint('appTurma', __name__)

##### GET all #####
@appTurma.route('/turmas', methods=['GET'])
def get_turmas():
    """Endpoint para buscar todas as turmas
    ---
    tags:
      - Turmas
    responses:
      200:
        description: Lista de turmas
      500:
        description: Erro de servidor
    """
    try:
        turmas = Turma.query.all()
        return jsonify([turma.serialize() for turma in turmas]), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro de servidor', 'erro': str(e)}), 500

##### GET ID #####
@appTurma.route('/turmas/<int:id>', methods=['GET'])
def get_turma(id):
    """Endpoint para buscar uma turma pelo ID
    ---
    tags:
      - Turmas
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Turma encontrada
      404:
        description: Turma não encontrada
      500:
        description: Erro de servidor
    """
    # Verificar Turma
    turma = Turma.query.get(id)
    if not turma:
        return jsonify({'message': 'Turma não encontrada!'}), 404
    try:
        return jsonify(turma.serialize()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro de servidor', 'erro': str(e)}), 500

##### POST #####
@appTurma.route('/turmas', methods=['POST'])
def post_turmas():
    """Endpoint para criar uma nova turma
    ---
    tags:
      - Turmas
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            descricao:
              type: string
            ativo:
              type: boolean
            professor_id:
              type: integer
    responses:
      201:
        description: Turma criada com sucesso
      400:
        description: Erro ao criar turma
      404:
        description: Professor não encontrado
      500:
        description: Erro de servidor
    """
    data = request.get_json()
    # Verifica se os dados foram enviados corretamente
    if not data or 'descricao' not in data or 'ativo' not in data:
        return jsonify({'message': 'Dados invalidos!'}), 400
    
    # Verifica se o professor existe
    professor_id = data.get('professor_id')
    if professor_id:
      if not db.session.query(Professor.id).filter_by(id=professor_id).scalar():
        return jsonify({'message': 'Professor não encontrado!'}), 404

    # Cria uma nova Turma
    nova_turma = Turma(
        descricao=data['descricao'],
        ativo=data['ativo'],
        professor_id=professor_id
    )

    try:
        # Adiciona a Turma no banco de Dados
        db.session.add(nova_turma)
        db.session.commit()
        return jsonify({'message': 'Turma criada com Sucesso!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro de servidor', 'erro': str(e)}), 500
    
##### PUT #####
@appTurma.route('/turmas/<int:id>', methods=['PUT'])
def put_turma(id):
    """Endpoint para atualizar dados de uma turma
    ---
    tags:
      - Turmas
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID da turma
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            descricao:
              type: string
            ativo:
              type: boolean
            professor_id:
              type: integer
    responses:
      200:
        description: Turma atualizada
      400:
        description: Erro ao atualizar turma
      404:
        description: Turma não encontrada
        description: Professor não encontrado
      500:
        description: Erro de servidor
    """
    data = request.get_json()
    
    # Verifica se os dados foram enviados corretamente
    if not data:
        return jsonify({'message': 'Dados invalidos!'}), 400
    
    # Verifica se a turma existe
    turma = Turma.query.get(id)
    if not turma:
        return jsonify({'message': 'Turma não encontrada!'}), 404
    
    if 'descricao' in data:
        turma.descricao = data['descricao']
    if 'ativo' in data:
        turma.ativo = data['ativo']
    if 'professor_id' in data:
        if not db.session.query(Professor.id).filter_by(id=data['professor_id']).scalar():
            return jsonify({'message': 'Professor não encontrado!'}), 404
        turma.professor_id = data['professor_id']
    
    try:
        # Atualiza a Turma no banco de Dados
        db.session.commit()
        return jsonify({'message': 'Turma atualizada com Sucesso!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro de servidor', 'erro': str(e)}), 500

##### DELETE #####
@appTurma.route('/turmas/<int:id>', methods=['DELETE'])
def delete_turma(id):
    """Endpoint para deletar uma turma
    ---
    tags:
      - Turmas
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID da turma
    responses:
      200:
        description: Turma deletada
      404:
        description: Turma não encontrada
      500:
        description: Erro de servidor
    """
    # Verifica se a turma existe
    turma = Turma.query.get(id)
    if not turma:
        return jsonify({'message': 'Turma não encontrada!'}), 404
    
    try:
        # Deleta a Turma do banco de Dados
        db.session.delete(turma)
        db.session.commit()
        return jsonify({'message': 'Turma deletada com Sucesso!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro de servidor', 'erro': str(e)}), 500

