from flask import Flask, request, jsonify, redirect, url_for
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
    return """
            <html>
                <body>
                    <a href="/peliculas">My Movie API</a>
                </body>
            </html>
            """


@app.route('/peliculas/', methods=["GET"])
def mostrar_peliculas():

    try:
        peliculas = Pelicula.query.all()

        if(not peliculas):
            return jsonify({"mensaje": "No hay peliculas cargadas"})
        
        peliculas_data = []
        
        for pelicula in peliculas:
            pelicula_data = {
                "id_pelicula": pelicula.id,
                "titulo": pelicula.titulo,
                "imagen": pelicula.imagen,
            }
            peliculas_data.append(pelicula_data)  

        return jsonify(peliculas_data)

    except Exception as error:
        print(error)
        return jsonify({"mensaje": "No se ha podido cargar ninguna pelicula"})
    

@app.route('/peliculas/', methods=["POST"])
def agregar_pelicula():

    try:
        nuevo_titulo = request.json.get("titulo")
        nueva_descripcion = request.json.get("descripcion")
        nuevo_genero_id = request.json.get("genero_id") 
        nuevo_director = request.json.get("director")
        nuevo_ano_lanzamiento = request.json.get("ano_lanzamiento")
        nueva_imagen = request.json.get("imagen")

        nueva_pelicula = Pelicula(titulo=nuevo_titulo, descripcion=nueva_descripcion, 
                                genero_id=nuevo_genero_id, director=nuevo_director, 
                                ano_lanzamiento=nuevo_ano_lanzamiento, imagen=nueva_imagen)
        db.session.add(nueva_pelicula)
        db.session.commit()
        
        return {"success": "pelicula agregada", "titulo": nuevo_titulo, "descripcion": nueva_descripcion,
                "id_genero": nuevo_genero_id, "director": nuevo_titulo, "ano lanzamiento": nuevo_ano_lanzamiento,
                "ruta imagen": nueva_imagen}

    except:
        return jsonify({"mensaje": "No se ha podido agregar la pelicula"})
    

@app.route('/peliculas/<id_pelicula>', methods=["GET"])
def mostrar_pelicula(id_pelicula):

    try:
        pelicula_seleccionada = db.session.query(Pelicula).join(Genero
        ).add_columns(Genero.nombre).filter(Pelicula.id == id_pelicula).first()
        
        pelicula = pelicula_seleccionada[0]
        nombre_genero = pelicula_seleccionada[1]

        pelicula_data = {
            "id_pelicula": pelicula.id,
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
    

@app.route('/peliculas/<id_pelicula>', methods=["PUT"])
def editar_pelicula(id_pelicula):

    try:
        nuevo_titulo = request.json.get("titulo")
        nueva_descripcion = request.json.get("descripcion")
        nuevo_genero_id = request.json.get("genero_id") 
        nuevo_director = request.json.get("director")
        nuevo_ano_lanzamiento = request.json.get("ano_lanzamiento")
        nueva_imagen = request.json.get("imagen")

        pelicula_editada = db.session.get(Pelicula, id_pelicula)

        pelicula_editada.titulo = nuevo_titulo    
        pelicula_editada.descripcion = nueva_descripcion
        pelicula_editada. genero_id = nuevo_genero_id
        pelicula_editada.director = nuevo_director
        pelicula_editada.ano_lanzamiento = nuevo_ano_lanzamiento
        pelicula_editada.imagen = nueva_imagen
        db.session.commit()
    
        return {"success": "pelicula editada exitosamente", "titulo": nuevo_titulo, "descripcion": nueva_descripcion,
                "id_genero": nuevo_genero_id, "director": nuevo_titulo, "ano lanzamiento": nuevo_ano_lanzamiento,
                "ruta imagen": nueva_imagen}

    except:
        return jsonify({"mensaje": "No se ha podido editar la pelicula seleccionada"})
    

@app.route('/peliculas/<id_pelicula>', methods=["DELETE"])
def eliminar_pelicula(id_pelicula):

    try:
        pelicula_a_eliminar = db.session.get(Pelicula, id_pelicula)
        
        actuaciones_a_eliminar = db.session.query(Actuacion).filter(Actuacion.pelicula_id == id_pelicula).all()
        
        for actuacion_a_eliminar in actuaciones_a_eliminar:
            interprete_a_eliminar = db.session.get(Interprete, actuacion_a_eliminar.interprete_id)
            db.session.delete( actuacion_a_eliminar)
            db.session.delete(interprete_a_eliminar)

        db.session.delete(pelicula_a_eliminar)
        db.session.commit()
        
        return jsonify({"success": "pelicula eliminada exitosamente"})

    except:
        return jsonify({"mensaje": "No se ha podido eliminar la pelicula seleccionada"})


@app.route('/peliculas/<id_pelicula>/reparto/', methods=["GET"])
def mostrar_interpretes(id_pelicula):

    try:
        interpretes = db.session.query(Interprete).join(Actuacion).join(Pelicula
        ).filter( Interprete.id == Actuacion.interprete_id,
        Actuacion.pelicula_id == Pelicula.id, Pelicula.id == id_pelicula).all()

        interpretes_data = []

        for interprete in interpretes:
            interprete_data = {
                "id_interprete": interprete.id,
                "nombre": interprete.nombre,
                "nacionalidad": interprete.nacionalidad,
                "fecha_nacimiento": interprete.fecha_nacimiento.isoformat(),
                "imagen": interprete.imagen,
                "interpretacion": interprete.nombre_interpretacion,
            }
            interpretes_data.append(interprete_data)  

        return jsonify(interpretes_data)

    except:
        return jsonify({"mensaje": "No se han podido cargar los interpretes "})
    

@app.route('/peliculas/<id_pelicula>/reparto/', methods=["POST"])
def agregar_interprete(id_pelicula):

    try:
        nuevo_nombre = request.json.get("nombre")
        nueva_nacionalidad = request.json.get("nacionalidad")
        nueva_fecha_nacimiento = request.json.get("fecha_nacimiento") 
        nueva_imagen = request.json.get("imagen")
        nueva_interpretacion = request.json.get("interpretacion")

        nuevo_interprete = Interprete(nombre=nuevo_nombre, nacionalidad=nueva_nacionalidad, 
                                fecha_nacimiento=nueva_fecha_nacimiento, imagen=nueva_imagen, 
                                nombre_interpretacion=nueva_interpretacion)
        db.session.add(nuevo_interprete)
        
        ultimo_interprete = Interprete.query.order_by(Interprete.id.desc()).first()

        nueva_actuacion = Actuacion(pelicula_id=id_pelicula, interprete_id=ultimo_interprete.id)
        db.session.add(nueva_actuacion)
        db.session.commit()

        return jsonify({"success": "interprete agregado exitosamente", "nombre": nuevo_nombre, "nacionalidad": nueva_nacionalidad,
                        "fecha nacimiento": nueva_fecha_nacimiento, "ruta imagen": nueva_imagen, 
                        "interpretacion": nueva_interpretacion})

    except:
        return jsonify({"mensaje": "No se ha podido agregar el interprete"})


@app.route('/peliculas/reparto/<id_interprete>', methods=["PUT"])
def editar_interprete(id_interprete):

    try:
        nuevo_nombre = request.json.get("nombre")
        nueva_nacionalidad = request.json.get("nacionalidad")
        nueva_fecha_nacimiento = request.json.get("fecha_nacimiento") 
        nueva_imagen = request.json.get("imagen")
        nueva_interpretacion = request.json.get("interpretacion")    
        
        interprete_editado = db.session.get(Interprete, id_interprete)
        
        interprete_editado.nombre = nuevo_nombre
        interprete_editado.nacionalidad = nueva_nacionalidad
        interprete_editado.fecha_nacimiento = nueva_fecha_nacimiento
        interprete_editado.imagen = nueva_imagen
        interprete_editado.nombre_interpretacion = nueva_interpretacion
        db.session.commit()
        
        return jsonify({"success": "interprete editado exitosamente", "nombre": nuevo_nombre, "nacionalidad": nueva_nacionalidad,
                        "fecha nacimiento": nueva_fecha_nacimiento, "ruta imagen": nueva_imagen, 
                        "interpretacion": nueva_interpretacion})

    except:
        return jsonify({"mensaje": "No se ha podido editar el interprete seleccionado "})
    

@app.route('/peliculas/reparto/<id_interprete>', methods=["DELETE"])
def eliminar_interprete(id_interprete):

    try:
        interprete_a_eliminar = db.session.get(Interprete, id_interprete)
        
        actuacion_a_eliminar = db.session.query(Actuacion).filter(Actuacion.interprete_id == id_interprete).first()
        
        db.session.delete(actuacion_a_eliminar)
        db.session.delete(interprete_a_eliminar)
        db.session.commit()
        
        return jsonify({"success": "interprete eliminado exitosamente"})

    except:
        return jsonify({"mensaje": "No se ha podido eliminar el interprete seleccionado"})


@app.route('/generos/', methods=["GET"])
def mostrar_generos():

    try:
        generos = db.session.query(Genero).all()
        
        generos_data = []

        for genero in generos:
            
            genero_data ={
                "id_genero": genero.id,
                "nombre": genero.nombre
            }
            generos_data.append(genero_data)
            
        return jsonify(generos_data)

    except:
        return jsonify({"mensaje": "No se han podido cargar los generos"})
    

@app.route('/interprete/<id_interprete>', methods=["GET"])
def mostrar_interprete(id_interprete):

    try:
        interprete = db.session.get(Interprete, id_interprete)
        
        interprete_data = {
            "nombre": interprete.nombre,
            "nacionalidad": interprete.nacionalidad,
            "fecha_nacimiento": interprete.fecha_nacimiento.isoformat(),
            "imagen": interprete.imagen,
            "interpretacion": interprete.nombre_interpretacion
        }

        return jsonify(interprete_data)

    except:
        return jsonify({"mensaje": "No se ha podido cargar el interprete"})


if __name__ == '__main__':
    print('Iniciando servidor...')
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)
    print('Iniciado...')
