from helpers.database import db
from flask_login import UserMixin

class Pets(UserMixin, db.Model):
  
  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String(50))
  idade = db.Column(db.String(4))
  especie = db.Column(db.String())
  observacoes = db.Column(db.String(500))
  