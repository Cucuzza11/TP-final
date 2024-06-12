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

class Interprete(db.Model):
    __tablename__ = 'interpretes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String[50], nullable=False)
    apellido = db.Column(db.String[50])
    nacionalidad = db.Column(db.String[50])
    fecha_nacimineto= db.Column(db.DateTime)
    imagen = db.Column(db.String[500], nullable=False)
    nombre_interpretacion = db.Column(db.String[50], nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.now())

class Actuacion(db.Model):
    __tablename__ = 'actuaciones'
    id = db.Column(db.Integer, primary_key=True)
    pelicula_id = db.Column(db.Integer, db.ForeignKey('peliculas.id'))
    interprete_id = db.Column(db.Integer, db.ForeignKey('interpretes.id'))
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.now())