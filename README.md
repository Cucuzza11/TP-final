# TP-final


## Grupo: Tommy Jerry y el gato

### Integrantes: Alex Sandro Escalante (110437), Nadia Iliana Crispino (110451)


## Resumen de TP

El trabajo contiene una lista de peliculas con un poco de informacion de cada una, que puede ser editada o eliminada, y a su vez se pueden agregar mas peliculas con su correspondiente informacion. 
Además, contiene un apartado en el cual se pueden ver los actores/actrices que participaron en cada pelicula, junto con el papel que representaron y un poco de su informacion personal. 
Al igual que en las peliculas, pueden ser agregados nuevos interpretes o eliminarse interpretes ya existentes de cada pelicula, y se puede editar la informacion de cada uno. 


## Backend

### Install

```bash
virtualenv venv
source venv/bin/activate
sudo apt-get install libpq-dev
cd backend
pip install -r requirements.txt
```

### Run

```bash
source venv/bin/activate
cd backend
python3 main.py
```


## Frontend

### Run

```bash
cd frontend
python3 -m http.server
```


## Base de Datos

Realizamos cuatro tablas para formar la base de datos. La primera tabla (genres) relacionada a los generos de las peliculas; la segunda tabla (films) relacionada a las peliculas, que utliza la tabla de generos para guardar el genero de cada pelicula; la tercera tabla (interpreters) relacionada a los interpretes; y la cuarta tabla (performances) que relaciona la tabla de peliculas con la tabla de interpretes.


<div align="center">
<img width="70%" src="img/diagrama">
</div>


La tabla genres puede parecer una tabla que se pudo haber evitado simplemente agregando un campo mas a la tabla films con el genero de cada una, pero el problema que tiene este modo es que no solo hay mas margen de equivocacion sino que, si un genero cambia su nombre es mas sencillo cambiarlo en la tabla genres que cambiarlo en cada campo de cada pelicula de la tabla films.
Al igual que la tabla genres, la tabla interpreters tiene su importancia ya que, si agregaramos mas campos a la tabla films unicamente para la informacion de cada interprete tendriamos dos opciones, agregar un solo interprete de cada pelicula o agregar varios interpretes pero los demas campos de la tabla films se repetirian, por lo que no seria lo mas optimo teniendo la opcion de poder agregar una tabla extra que almacene cada interprete con su informacion. Es asi que, la tabla performances relaciona la tabla de peliculas y la de interpretes, almacenando que interprete pertenece a que pelicula.