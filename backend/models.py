import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Genero(db.Model):
    __tablename__ = 'generos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String[50], nullable=False)
    
