from flask import Flask, request, jsonify
from models import db, Genre, Film, Interpreter, Performance
from flask_cors import CORS
from datetime import datetime

FIRST_FILM_YEAR = 1895
CURRENT_YEAR = 2024


app = Flask(__name__)
CORS(app)
port = 5000
app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://nadia:Nadia1108@localhost:5432/tp'
#app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://alex:Alex0103@localhost:5432/tp'
#app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://tp:123456@localhost:5432/BDtp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

@app.route('/')
def hello_world():
    return """
            <html>
                <body>
                    <a href="/films">My Films API</a>
                </body>
            </html>
            """


@app.route('/films/', methods=["GET"])
def show_films():

    try:
        films = db.session.query(Film).order_by(Film.title).all()

        if(not films):
            return jsonify({"message": "No hay peliculas cargadas"})
        
        films_data = []
        
        for film in films:
            film_data = {
                "film_id": film.id,
                "title": film.title,
                "image": film.image
            }
            films_data.append(film_data)  

        return jsonify(films_data)

    except Exception as error:
        print(error)
        return jsonify({"message": "No se han podido cargar las peliculas debido a un error"})
    

@app.route('/films/', methods=["POST"])
def add_film():

    try:
        new_title = request.json.get("title")
        new_description = request.json.get("description")
        new_genre_id = request.json.get("genre_id") 
        new_director = request.json.get("director")
        new_release_year = int(request.json.get("release_year"))
        new_image = request.json.get("image")

        if(not new_title or not new_description or not new_genre_id or not new_director
            or not new_release_year or not new_image):
            return({"message": "Datos incompletos"})

        if(new_release_year < FIRST_FILM_YEAR or new_release_year > CURRENT_YEAR):
            return jsonify({"message": "El ano ingresado no es valido"})

        new_film = Film(title=new_title, description=new_description, 
                        genre_id=new_genre_id, director=new_director, 
                        release_year=new_release_year, image=new_image)
        
        db.session.add(new_film)
        db.session.commit()
        
        return jsonify({"success": "pelicula agregada", "titulo": new_title, "descripcion": new_description,
                "id_genero": new_genre_id, "director": new_director, "ano lanzamiento": new_release_year,
                "ruta imagen": new_image})

    except Exception as error:
        print(error)
        return jsonify({"message": "No se ha podido agregar la pelicula debido a un error"})
    

@app.route('/films/<film_id>', methods=["GET"])
def show_film(film_id):

    try:
        selected_film = db.session.query(Film, Genre).filter(
            Film.id == film_id, Film.genre_id == Genre.id).first()
        
        if(not selected_film):
            return jsonify({"message": "la pelicula seleccionada no existe"})

        film = selected_film[0]
        genre = selected_film[1]

        film_data = {
            "film_id": film.id,
            "title": film.title,
            "description": film.description,
            "genre_id": genre.id,
            "genre_name": genre.name,
            "director": film.director,
            "release_year": film.release_year,
            "image": film.image
        }  
        
        return jsonify({"film": film_data})

    except Exception as error:
        print(error)
        return jsonify({"message": "No se ha podido cargar la pelicula debido a un error"})
    

@app.route('/films/<film_id>', methods=["PUT"])
def edit_film(film_id):

    try:
        new_title = request.json.get("title")
        new_description = request.json.get("description")
        new_genre_id = request.json.get("genre_id") 
        new_director = request.json.get("director")
        new_release_year = int(request.json.get("release_year"))
        new_image = request.json.get("image")

        if(not new_title or not new_description or not new_genre_id or not new_director
            or not new_release_year or not new_image):
            return jsonify({"message": "Datos incompletos"})

        if(new_release_year < FIRST_FILM_YEAR or new_release_year > CURRENT_YEAR):
            return jsonify({"message": "El ano ingresado no es valido"})

        edited_film = db.session.get(Film, film_id)

        if(not edited_film):
            return jsonify({"message": "La pelicula que desea editar no existe"})

        edited_film.title = new_title    
        edited_film.description = new_description
        edited_film.genre_id = new_genre_id
        edited_film.director = new_director
        edited_film.release_year = new_release_year
        edited_film.image = new_image
        db.session.commit()
    
        return jsonify({"success": "pelicula editada exitosamente", "titulo": new_title, "descripcion": new_description,
                "id genero": new_genre_id, "director": new_director, "ano lanzamiento": new_release_year,
                "ruta imagen": new_image})

    except Exception as error:
        print(error)
        return jsonify({"message": "No se ha podido editar la pelicula debido a un error"})
    

@app.route('/films/<film_id>', methods=["DELETE"])
def delete_film(film_id):

    try:
        film_to_remove = db.session.get(Film, film_id)
        
        if(not film_to_remove):
            return jsonify({"message": "La pelicula que desea eliminar no existe"})

        performances_to_remove = db.session.query(Performance).filter(Performance.film_id == film_id).all()
        
        if(performances_to_remove):
            for performance_to_remove in performances_to_remove:
                interpreter_to_remove = db.session.get(Interpreter, performance_to_remove.interpreter_id)
                db.session.delete( performance_to_remove)
                db.session.commit()
                db.session.delete(interpreter_to_remove)
                db.session.commit()

        db.session.delete(film_to_remove)
        db.session.commit()
        
        return jsonify({"success": "pelicula eliminada exitosamente", "id pelicula": film_id})

    except Exception as error:
        print(error)
        return jsonify({"message": "No se ha podido eliminar la pelicula debido a un error"})


@app.route('/films/<film_id>/cast/', methods=["GET"])
def show_cast(film_id):

    try:
        film = db.session.get(Film, film_id)

        if(not film):
            return jsonify({"message": "La pelicula de la cual desea ver sus interpretes no existe"})

        interpreters = db.session.query(Interpreter).order_by(Interpreter.name).join(Performance).join(Film
            ).filter( Interpreter.id == Performance.interpreter_id, Performance.film_id == Film.id, 
            Film.id == film_id).all()

        if(not interpreters):
            return jsonify({"message": "No hay interpretes cargados"})

        interpreters_data = []

        for interpreter in interpreters:
            interpreter_data = {
                "interpreter_id": interpreter.id,
                "name": interpreter.name,
                "nationality": interpreter.nationality,
                "birthdate": interpreter.birthdate.isoformat() if interpreter.birthdate else None,
                "image": interpreter.image,
                "interpretation": interpreter.interpretation_name
            }
            interpreters_data.append(interpreter_data)  

        return jsonify(interpreters_data)

    except Exception as error:
        print(error)
        return jsonify({"message": "No se han podido cargar los interpretes debido a un error"})
    

def valid_date(date):
    try: 
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except:
        return False


@app.route('/films/<film_id>/cast/', methods=["POST"])
def add_interpreter(film_id):

    try:
        film = db.session.get(Film, film_id)

        if(not film):
            return jsonify({"message": "La pelicula a la que desea agregar un interprete no existe"})

        new_name = request.json.get("name")
        new_nationality = request.json.get("nationality")
        new_birthdate = None
        if(request.json.get("birthdate")):
            new_birthdate =  request.json.get("birthdate")
        new_image = request.json.get("image")
        new_interpretation = request.json.get("interpretation")

        if(not new_name or not new_image or not new_interpretation):
            return jsonify({"message": "Datos incompletos"})

        if(new_birthdate and not valid_date(new_birthdate)):
            return jsonify({"message": "La fecha ingresada es incorrecta"})

        new_interpreter = Interpreter(name=new_name, nationality=new_nationality, 
            birthdate=new_birthdate, image=new_image, interpretation_name=new_interpretation)
        
        db.session.add(new_interpreter)
        
        last_interpreter = Interpreter.query.order_by(Interpreter.id.desc()).first()

        new_performance = Performance(film_id=film_id, interpreter_id=last_interpreter.id)
        db.session.add(new_performance)
        db.session.commit()

        return jsonify({"success": "interprete agregado exitosamente", "nombre": new_name, "nacionalidad": new_nationality,
                        "fecha nacimiento": new_birthdate, "ruta imagen": new_image, "interpretacion": new_interpretation})

    except Exception as error:
        print(error)
        return jsonify({"message": "No se ha podido agregar el interprete debido a un error"})


@app.route('/films/<film_id>/cast/<interpreter_id>', methods=["PUT"])
def edit_interpreter(film_id, interpreter_id):

    try:
        film = db.session.get(Film, film_id)

        if(not film):
            return jsonify({"message": "La pelicula del interprete que desea editar no existe"})

        new_name = request.json.get("name")
        new_nationality = request.json.get("nationality")
        new_birthdate = None
        if(request.json.get("birthdate")):
            new_birthdate = request.json.get("birthdate") 
        new_image = request.json.get("image")
        new_interpretation = request.json.get("interpretation")    
        
        if(not new_name or not new_image or not new_interpretation):
            return jsonify({"message": "Datos incompletos"})

        if(new_birthdate and not valid_date(new_birthdate)):
            return jsonify({"message": "La fecha ingresada es incorrecta"})

        edited_interpreter = db.session.get(Interpreter, interpreter_id)
        
        if(not edited_interpreter):
            return jsonify({"message": "El interprete que desea editar no existe"})

        edited_interpreter.name = new_name
        edited_interpreter.nationality = new_nationality
        edited_interpreter.birthdate = new_birthdate
        edited_interpreter.image = new_image
        edited_interpreter.interpretation_name = new_interpretation
        db.session.commit()
        
        return jsonify({"success": "interprete editado exitosamente", "nombre": new_name, "nacionalidad": new_nationality,
                        "fecha nacimiento": new_birthdate, "ruta imagen": new_image, "interpretacion": new_interpretation})

    except Exception as error:
        print(error)
        return jsonify({"message": "No se ha podido editar el interprete seleccionado debido a un error"})
    

@app.route('/films/cast/<interpreter_id>', methods=["DELETE"])
def delete_interpreter(interpreter_id):

    try:
        interpreter_to_remove = db.session.get(Interpreter, interpreter_id)
        
        if(not interpreter_to_remove):
            return jsonify({"message": "El interprete que desea eliminar no existe"})
    
        performance_to_remove = db.session.query(Performance).filter(Performance.interpreter_id == interpreter_id).first()
        
        db.session.delete(performance_to_remove)
        db.session.commit()
        db.session.delete(interpreter_to_remove)
        db.session.commit()
        
        return jsonify({"success": "interprete eliminado exitosamente"})

    except Exception as error:
        print(error)
        return jsonify({"message": "No se ha podido eliminar el interprete seleccionado debido a un error"})


@app.route('/genres/', methods=["GET"])
def show_genres():

    try:
        genres = db.session.query(Genre).order_by(Genre.name).all()
        
        if(not genres):
            return jsonify({"message": "No hay generos cargados"})

        genres_data = []

        for genre in genres:
            genre_data ={
                "genre_id": genre.id,
                "name": genre.name
            }
            genres_data.append(genre_data)
            
        return jsonify(genres_data)

    except Exception as error:
        print(error)
        return jsonify({"message": "No se han podido cargar los generos debido a un error"})
    

@app.route('/interpreter/<interpreter_id>', methods=["GET"])
def show_interpreter(interpreter_id):

    try:
        interpreter = db.session.get(Interpreter, interpreter_id)
        
        if(not interpreter):
            return jsonify({"message": "El interprete seleccionado no existe"})

        interpreter_data = {
            "name": interpreter.name,
            "nationality": interpreter.nationality,
            "birthdate": interpreter.birthdate.isoformat() if interpreter.birthdate else None,
            "image": interpreter.image,
            "interpretation": interpreter.interpretation_name
        }

        return jsonify({"interpreter": interpreter_data})

    except Exception as error:
        print(error)
        return jsonify({"message": "No se ha podido cargar el interprete debido a un error"})


if __name__ == '__main__':
    print('Iniciando servidor...')
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)
    print('Iniciado...')
