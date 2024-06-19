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
    

@app.route('/peliculas/<id_pelicula>', methods=["GET"])
def mostrar_pelicula(id_pelicula):

    try:
        pelicula_seleccionada = db.session.query(Pelicula).join(Genero
        ).add_columns(Genero.nombre).filter(Pelicula.id == id_pelicula).first()
        
        pelicula = pelicula_seleccionada[0]
        nombre_genero = pelicula_seleccionada[1]

        pelicula_data = {
            "id": pelicula.id,
            "titulo": pelicula.titulo,
            "descripcion": pelicula.descripcion,
            "genero": nombre_genero,
            "director": pelicula.director,
            "ano_lanzamiento": pelicula.ano_lanzamiento,
            "imagen": pelicula.imagen
        }     
        return jsonify(pelicula_data)

    except:
        return jsonify({"mensaje": "No se ha podido cargar la pelicula seleccionada"})
    

@app.route('/peliculas/<id_pelicula>/reparto/', methods=["GET"])
def mostrar_interpretes(id_pelicula):

    try:
        interpretes = db.session.query(Interprete).join(Actuacion).join(Pelicula
        ).filter( Interprete.id == Actuacion.interprete_id,
        Actuacion.pelicula_id == Pelicula.id, Pelicula.id == id_pelicula).all()

        interpretes_data = []
        
        for interprete in interpretes:
            interprete_data = {
                "id": interprete.id,
                "imagen": interprete.imagen,
                "interpretacion": interprete.nombre_interpretacion,
            }
            interpretes_data.append(interprete_data)      
        return jsonify(interpretes_data)

    except:
        return jsonify({"mensaje": "No se han podido cargar los interpretes "})
    

if __name__ == '__main__':
    print('Iniciando servidor...')
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)
    print('Iniciado...')
