import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String[50], nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.datetime.now())
    
class Film(db.Model):
    __tablename__ = 'films'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String[50], nullable=False)
    description = db.Column(db.String[500], nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'))
    director = db.Column(db.String[50], nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String[500], nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.datetime.now())

class Interpreter(db.Model):
    __tablename__ = 'interpreters'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String[50], nullable=False)
    nationality = db.Column(db.String[50])
    birthdate = db.Column(db.Date)
    image = db.Column(db.String[500], nullable=False)
    interpretation_name = db.Column(db.String[50], nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.datetime.now())

class Performance(db.Model):
    __tablename__ = 'performances'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    film_id = db.Column(db.Integer, db.ForeignKey('films.id'))
    interpreter_id = db.Column(db.Integer, db.ForeignKey('interpreters.id'))
    creation_date = db.Column(db.DateTime, default=datetime.datetime.now())