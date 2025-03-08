from database import db
from models.professor import Professor

class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    ativo = db.Column(db.Boolean, nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=True)

    # Relacionamento
    professor = db.relationship('Professor', backref='turmas')

    def serialize(self):
        return {
            'id': self.id,
            'descricao': self.descricao,
            'ativo': self.ativo,
            'professor_id': self.professor_id
        }