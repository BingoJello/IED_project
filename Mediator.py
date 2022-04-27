from sparQL import requestSparQL as sparql
from service import ClientREST
from database import DatabaseQuery
from model.Film import Film

def getInfoByFilm(title):
    films_request = []

    #Récupération des films de la base de données
    films_db = DatabaseQuery.selectQuery(title)
    #Récupération des films de la source DBpedia via SparQL
    films_sparql = sparql.requestFilmByTitle(title)

    for film in films_db :
        films_request.append(film)

    #Fusion des films de la base de données et des films de la source DBpedia

    #Cas ou la source DBpedia à renvoyée des résultats
    if len(films_sparql) > 1 :
        films_join = []
        for film_sparql in films_sparql :
            exist_in_db = False
            for film_request in films_request :
                year = film_request.get_release_date().split("/")[2]
                if film_sparql.get_year() == year :
                    film_request.set_directors(film_sparql.get_directors())
                    film_request.set_actors(film_sparql.get_actors())
                    film_request.set_producers(film_sparql.get_producers())
                    film_request.set_year(film_sparql.get_year())

                    for distributor in film_sparql.get_distributors():
                        if distributor not in film_request.get_distributors():
                            film_request.get_distributors().append(distributor)
                    film_request.set_distributors([ele for ele in film_request.get_distributors() if ele.strip()])
                    exist_in_db = True
                    break
            if exist_in_db == False :
                films_join.append(film_sparql)

        if len(films_join) > 0 :
            for film_sparql in films_join :
                film = Film()
                film.set_name(film_sparql.get_name())
                film.set_directors(film_sparql.get_directors())
                film.set_actors(film_sparql.get_actors())
                film.set_producers(film_sparql.get_producers())
                film.set_year(film_sparql.get_year())
                film.set_distributors(film_sparql.get_distributors())
                films_request.append(film)

    #Cas ou la source DBpedia n'a renvoyée aucun résultat
    else :
        if len(films_request) > 0 and len(films_sparql) > 0 :
            for film_request in films_request :
                if film_request.get_name() == "" :
                    film_request.set_name(films_sparql[0].get_name())
                film_request.set_directors(films_sparql[0].get_directors())
                film_request.set_actors(films_sparql[0].get_actors())
                film_request.set_producers(films_sparql[0].get_producers())
        elif len(films_sparql) > 0 :
            films_request.append(films_sparql[0])

    #Récupération des films via le web service REST
    films_request = ClientREST.getRequest(films_request, title)

    return films_request

def getInfoByActor(name_actor):
    films_request = []
    # Récupération des films de la source Dbpedia
    films_sparql = sparql.requestFilmByByActor(name_actor)

    for film_sparql in films_sparql:
        films_request.append(film_sparql)

    films_request_tmp = []

    # Récupération des films de la base de données pour chaque film de la source Dbpedia
    for film_sparql in films_request:
        films_db = DatabaseQuery.selectQuery(film_sparql.get_name())
        cache_film = []

        for film_db in films_db:
            if film_db.get_name() == film_sparql.get_name():
                release_date = film_db.get_release_date().split('/')[2]
                if film_sparql.get_year() != "":
                    if release_date == film_sparql.get_year():
                        film_sparql.set_release_date(film_db.get_release_date())
                        film_sparql.set_production_budget(film_db.get_production_budget())
                        film_sparql.set_domestic_gross(film_db.get_domestic_gross())
                        film_sparql.set_worldwide_gross(film_db.get_worldwide_gross())
                        film_sparql.set_genre(film_db.get_genre())
                        distributors = []
                        for distributor in film_sparql.get_distributors() :
                            if distributor not in film_db.get_distributors() :
                                distributors.append(distributor)

                        if len(distributors) > 0:
                            film_sparql.get_distributors().extend(distributors)

                        cache_film.append(film_db)
                else:
                    film_sparql.set_release_date(film_db.get_release_date())
                    film_sparql.set_production_budget(film_db.get_production_budget())
                    film_sparql.set_domestic_gross(film_db.get_domestic_gross())
                    film_sparql.set_worldwide_gross(film_db.get_worldwide_gross())
                    film_sparql.set_genre(film_db.get_genre())
                    distributors = []
                    for distributor in film_sparql.get_distributors() :
                        if distributor not in film_db.get_distributors() :
                            distributors.append(distributor)

                    if len(distributors) > 0 :
                        film_sparql.get_distributors().extend(distributors)

                    cache_film.append(film_db)
                break

        for film_db in films_db:
            if film_db not in cache_film:
                films_request_tmp.append(film_db)

    films_request.extend(films_request_tmp)


    #Récupération des films du web service REST
    films_request = ClientREST.getRequest(films_request)

    return films_request


