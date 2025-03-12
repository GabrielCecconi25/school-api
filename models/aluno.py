from database import db

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    nota_primeiro_semestre = db.Column(db.Float, nullable=True)
    nota_segundo_semestre = db.Column(db.Float, nullable=True)
    media_final = db.Column(db.Float, nullable=True)
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=True)

    # Relacionamento
    turma = db.relationship('Turma', backref='alunos')

    def serialize(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'idade': self.idade,
            'nota_primeiro_semestre': self.nota_primeiro_semestre,
            'nota_segundo_semestre': self.nota_segundo_semestre,
            'turma_id': self.turma_id
        }