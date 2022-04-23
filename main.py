from sparQL import requestSparQL as spark
from service import ClientREST
from database import DatabaseQuery
from model.Film import Film
films_db = DatabaseQuery.selectQuery("Godzilla")
print("----Film BD----")
for film in films_db :
    print(film.get_name(), film.get_release_date(), film.get_worldwide_gross(), film.get_directors(), film.get_producers(), film.get_actors())

print("\n----Film Spark----")
films_spark = spark.requestFilmByTitle("Godzilla")
for film in films_spark :
    print(film.get_name(), film.get_year(), film.get_directors(), film.get_producers(), film.get_actors())

print("\n----Film Rest----")
film_rest = ClientREST.getRequest("Godzilla")
print(film.get_name(), film.get_year(), film.get_directors(), film.get_actors())

print("\n----Fusion----")
films_request = []
for film in films_db :
    films_request.append(film)

if len(films_spark) > 2:
    films_to_insert = []
    for film_spark in films_spark :
        exist_db = False
        for film_request in films_request :
            year = film_request.get_release_date().split("/")[2]
            if film_spark.get_year() == year :
                film_request.set_directors(film_spark.get_directors())
                film_request.set_actors(film_spark.get_actors())
                film_request.set_producers(film_spark.get_producers())
                exist_db = True
                break
        if exist_db == False:
            films_to_insert.append(film_spark)

    if len(films_to_insert) > 0 :
        for film_spark in films_to_insert:
            film = Film()
            film.set_name(film_spark.get_name())
            film.set_directors(film_spark.get_directors())
            film.set_actors(film_spark.get_actors())
            film.set_producers(film_spark.get_producers())
            films_request.append(film)
else:
    index = 0
    for film_request in films_request :
        film_request.set_directors(films_spark[0].get_directors())
        film_request.set_actors(films_spark[0].get_actors())
        film_request.set_producers(films_spark[0].get_producers())
    index += 1
#ClientREST.getRequest("Insidious")


for film in films_request :
    print(film.get_name(), film.get_release_date(), film.get_worldwide_gross(), film.get_directors(), film.get_producers(), film.get_actors())
