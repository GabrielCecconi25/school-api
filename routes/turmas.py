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
    
    professor_id = data.get('professor_id')

    if professor_id:
      if not db.session.query(Professor.id).filter_by(id=professor_id).scalar():
        return jsonify({'message': 'Professor não encontrado!'}), 404

    print('teste')
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