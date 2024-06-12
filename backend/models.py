import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Genero(db.Model):
    __tablename__ = 'generos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String[50], nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.now())
    
class Pelicula(db.Model):
    __tablename__ = 'peliculas'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String[50], nullable=False)
    descripcion = db.Column(db.String[500], nullable=False)
    genero_id = db.Column(db.Integer, db.ForeignKey('generos.id'))
    director = db.Column(db.String[50], nullable=False)
    fecha_lanzamiento = db.Column(db.DateTime, nullable=False)
    imagen = db.Column(db.String[500], nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.now())