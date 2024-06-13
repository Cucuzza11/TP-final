from flask import Flask, request, jsonify
from models import db, Genero, Pelicula, Interprete, Actuacion
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
port = 5000
#app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://nadia:Nadia1108@localhost:5432/tp'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://alex:Alex0103@localhost:5432/tp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

@app.route('/')
def hola_mundo():
    return 'Hola mundo'

@app.route('/peliculas/', methods=["GET"])
def mostrar_peliculas():

    try:
        peliculas = Pelicula.query.all()

        peliculas_data = []
        
        for pelicula in peliculas:
            pelicula_data = {
                "id": pelicula.id,
                "titulo": pelicula.titulo,
                "imagen": pelicula.imagen,
            }
            peliculas_data.append(pelicula_data)  

        return jsonify(peliculas_data)

    except:
        return jsonify({"mensaje": "No se ha podido cargar ninguna pelicula"})
    

if __name__ == '__main__':
    print('Iniciando servidor...')
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)
    print('Iniciado...')