from flask import Blueprint, request, jsonify

from models.aluno import Aluno
from database import db

appAluno = Blueprint('appAluno', __name__)

##### GET all #####
@appAluno.route('/alunos', methods=['GET'])
def get_alunos():
    """Endpoint para buscar todos os alunos
    ---
    tags:
      - Alunos
    responses:
      200:
        description: Lista de alunos
      500:
        description: Erro de servidor
    """
    try:
        alunos = Aluno.query.all()
        return jsonify([aluno.serialize() for aluno in alunos]), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro de servidor', 'erro': str(e)}), 500
    
##### GET by id #####
@appAluno.route('/alunos/<int:id>', methods=['GET'])
def get_aluno(id):
    """Endpoint para buscar um aluno por id
    ---
    tags:
      - Alunos
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do aluno
    responses:
      200:
        description: Aluno encontrado
      404:
        description: Aluno não encontrado
      500:
        description: Erro de servidor
    """
    try:
        aluno = Aluno.query.get(id)
        if not aluno:
            return jsonify({'message': 'Aluno não encontrado'}), 404
        
        return jsonify(aluno.serialize()), 200
      
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro de servidor', 'erro': str(e)}), 500

##### POST #####
@appAluno.route('/alunos', methods=['POST'])
def post_aluno():
    """Endpoint para criar um aluno
    ---
    tags:
      - Alunos
    parameters:
        - name: body
            in: body
            required: true
            schema:
            id: Aluno
            properties:
                nome:
                type: string
                example: João
                idade:
                type: integer
                example: 15
                data_nascimento:
                type: string
                example: 2005-01-01
                nota_primeiro_semestre:
                type: float
                example: 7.5
                nota_segundo_semestre:
                type: float
                example: 8.0
                turma_id:
                type: integer
                example: 1
    responses:
      201:
        description: Aluno criado
      400:
        description: Erro de validação
      500:
        description: Erro de servidor
    """
