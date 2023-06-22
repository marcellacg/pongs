from helpers.database import db
from flask_login import UserMixin


class PasseioParque(UserMixin, db.Model):

    __tablename__ = 'passeio_parque'

    id = db.Column(db.Integer, primary_key=True)
    data_inicial = db.Column(db.String(20))
    data_final = db.Column(db.String(20))
    hora_inicial = db.Column(db.String(20))
    hora_final = db.Column(db.String(20))
    telefone = db.Column(db.String(11))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship("User", uselist=False)

    def __init__(self, data_inicial, data_final, hora_inicial, hora_final, telefone, user):
        self.data_inicial = data_inicial
        self.data_final = data_final
        self.hora_inicial = hora_inicial
        self.hora_final = hora_final
        self.telefone = telefone
        self.user = user
