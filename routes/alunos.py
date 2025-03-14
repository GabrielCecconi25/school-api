from flask import Blueprint, request, jsonify
from datetime import datetime

from models.aluno import Aluno
from models.turma import Turma
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
          type: object
          properties:
            nome:
              type: string
              example: Gabriel Silva
            idade:
              type: integer
              example: 15
            data_nascimento:
              type: string
              example: YYYY-MM-DD
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
      404:
        description: Truma não encontrada
      500:
        description: Erro de servidor
    """
    data = request.get_json()
    
    if not data or 'nome' not in data or 'idade' not in data or 'data_nascimento' not in data:
        return jsonify({'message': 'Dados inválidos'}), 400
    
    # Verifica se a turma existe
    if 'turma_id' in data:
        if not db.session.query(Turma.id).filter_by(id=data['turma_id']).scalar():
            return jsonify({'message': 'Turma não encontrada'}), 404
    
    try:
        # Converte a data de nascimento para o formato Date
        data_nascimento = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()

        nota_primeiro_semestre = data.get('nota_primeiro_semestre')
        nota_segundo_semestre = data.get('nota_segundo_semestre')
        # Calcula a média final
        media_final = None
        if nota_primeiro_semestre is not None and nota_segundo_semestre is not None:
            media_final = (nota_primeiro_semestre + nota_segundo_semestre) / 2

        # Cria um novo aluno
        novo_aluno = Aluno(
            nome=data['nome'],
            idade=data['idade'],
            data_nascimento=data_nascimento,
            nota_primeiro_semestre=nota_primeiro_semestre,
            nota_segundo_semestre=nota_segundo_semestre,
            media_final=media_final,
            turma_id=data.get('turma_id')
        )

        # Adiciona aluno ao banco de dados
        db.session.add(novo_aluno)
        db.session.commit()
        return jsonify({'message': 'Aluno criado com sucesso!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro de servidor', 'erro': str(e)}), 500


##### PUT #####
@appAluno.route('/alunos/<int:id>', methods=['PUT'])
def put_aluno(id):
    """Endpoint para atualizar um aluno
    ---
    tags:
      - Alunos
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do aluno
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: Gabriel Silva
            idade:
              type: integer
              example: 15
            data_nascimento:
              type: string
              example: YYYY-MM-DD
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
      200:
        description: Aluno atualizado
      400:
        description: Erro de validação
      404:
        description:
          - Aluno não encontrado
          - Turma não encontrada
      500:
        description: Erro de servidor
    """
    data = request.get_json()

    # Verifica se os dados foram enviados corretamente
    if not data:
        return jsonify({'message': 'Dados inválidos'}), 400
    
    aluno = Aluno.query.get(id)

    # Verifica se o aluno existe
    if not aluno:
        return jsonify({'message': 'Aluno não encontrado'}), 404
    
    # Verificação de notas e média
    if 'nota_primeiro_semestre' in data or 'nota_segundo_semestre' in data:
        if 'nota_primeiro_semestre' in data:
            aluno.nota_primeiro_semestre = data['nota_primeiro_semestre']
        if 'nota_segundo_semestre' in data:
            aluno.nota_segundo_semestre = data['nota_segundo_semestre']

        if aluno.nota_primeiro_semestre is not None and aluno.nota_segundo_semestre is not None:
            aluno.media_final = (aluno.nota_primeiro_semestre + aluno.nota_segundo_semestre) / 2
        else:
            aluno.media_final = None

    if 'turma_id' in data:
        # Verifica se a turma existe
        if not db.session.query(Turma.id).filter_by(id=data['turma_id']).scalar():
            return jsonify({'message': 'Turma não encontrada'}), 404
        aluno.turma_id = data['turma_id']
    if 'nome' in data:
        aluno.nome = data['nome']
    if 'idade' in data:
        aluno.idade = data['idade']
    if 'data_nascimento' in data:
        aluno.data_nascimento = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()
    
    try:
        # Atualiza o Aluno no Banco de Dados
        db.session.commit()
        return jsonify({'message': 'Aluno atualizado com sucesso!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro de servidor', 'erro': str(e)}), 500

##### DELETE #####
@appAluno.route('/alunos/<int:id>', methods=['DELETE'])
def delete_aluno(id):
    """Endpoint para deletar um aluno
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
        description: Aluno deletado
      404:
        description: Aluno não encontrado
      500:
        description: Erro de servidor
    """
    aluno = Aluno.query.get(id)

    # Verifica se o aluno existe
    if not aluno:
        return jsonify({'message': 'Aluno não encontrado'}), 404
    
    try:
        # Deleta o Aluno do banco de Dados
        db.session.delete(aluno)
        db.session.commit()
        return jsonify({'message': 'Aluno deletado com sucesso!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro de servidor', 'erro': str(e)}), 500
