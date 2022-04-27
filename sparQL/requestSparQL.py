from SPARQLWrapper import SPARQLWrapper, JSON, XML
import json
import xml.etree.ElementTree as ET
from model.Film import Film

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def requestFilmByTitle(title):
    list_films = getNumberFilm(title)
    directors = getDirectorsByFilm(title, list_films)
    actors = getActorsByFilm(title, list_films)
    producers = getProducersByFilm(title, list_films)
    distributors = getDistributorByFilm(title, list_films)

    if len(directors['director']) <= 0 or len(actors['actor']) <= 0 or len(producers['producer']) <= 0 or len(distributors['distributor']) <= 0:
        return []

    request_films = []

    if list_films > 1 :
        years = getYearFilms(title)
        for i in range(0, len(years)) :
            film = Film()
            film.set_year(years[i])
            film.set_name(title)
            request_films.append(film)
    else:
        film = Film()
        film.set_name(title)
        request_films.append(film)

    index = 0

    for director in directors['director'] :
        if list_films > 1 :
            for film in request_films :
                if film.get_year() == directors['year_film'][index] :
                    film.get_directors().append(director)
                    break
        else :
            request_films[0].get_directors().append(director)
        index += 1

    index = 0
    for actor in actors['actor']:
        if list_films > 1 :
            for film in request_films :
                if film.get_year() == actors['year_film'][index] :
                    film.get_actors().append(actor)
                    break
        else :
            request_films[0].get_actors().append(actor)
        index += 1

    index = 0
    for producer in producers['producer'] :
        if list_films > 1 :
            for film in request_films :
                if film.get_year() == producers['year_film'][index] :
                    film.get_producers().append(producer)
                    break
        else :
            request_films[0].get_producers().append(producer)
        index += 1

    index = 0

    for distributor in distributors['distributor'] :
        if list_films > 1 :
            for film in request_films :
                if film.get_year() == distributors['year_film'][index] :
                    film.get_distributors().append(distributor)
                    break
        else :
            request_films[0].get_distributors().append(distributor)
        index += 1

    return request_films

def requestFilmByByActor(name_actor):
    films_request = []

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    sparql.setQuery('SELECT DISTINCT(?film) ?title ?director ?producer ?distributor WHERE {'
                        '?film a dbo:Film ;'
                        'foaf:name ?title;'
                        'dbo:director ?d ;'
                        'dbo:starring ?a ;'
                        'dbo:producer ?p ;'
                        'dbo:distributor ?di.'
                        '?d foaf:name ?director .'
                        '?p foaf:name ?producer.'
                        '?di foaf:name ?distributor .'
                        '?a foaf:name "'+name_actor+'"@en .'
                        'optional { ?distributor dbo:distributor ?di .}'
                        'optional { ?producer dbo:producer ?p .}'
                        'optional { ?director dbo:director ?d  .}'
                    '}'
                    'GROUP BY(?film)'
                    'ORDER BY(?film)')


    sparql.setReturnFormat(JSON)
    results = sparql.queryAndConvert()

    cache_film = []

    for r in results["results"]['bindings']:
        film_link = r['film']['value'].split('resource/')[1]
        year = ""

        if "_(" in film_link:
            print(film_link)
            film_link = film_link.split('_(')[0]

            if has_numbers(film_link[1]) and len(film_link[1].split('_')[0]) == 4:
                year = film_link[1].split('_')[0]

        film_link = film_link.replace("_", " ")
        title = r['title']['value']
        director = r['director']['value']
        producer = r['producer']['value']
        distributor = r['distributor']['value']

        if title not in cache_film :
            cache_film.append(title)
            film = Film()
            film.set_name(title)
            film.set_year(year)
            film.get_directors().append(director)
            film.get_producers().append(producer)
            film.get_distributors().append(distributor)
            films_request.append(film)
        else :
            find = False
            for film_request in films_request:
                if film_link == film_request.get_name() :
                    if director in film_request.get_directors():
                        if producer in film_request.get_producers():
                            if distributor not in film_request.get_distributors():
                                film_request.get_distributors().append(distributor)
                        else:
                            film_request.get_producers().append(producer)
                    else:
                        film_request.get_directors().append(director)
                    find = True
                    break

            if find == False:
                cache_film.append(film_link)
                film = Film()
                film.set_name(film_link)
                film.set_year(year)
                film.get_directors().append(director)
                film.get_producers().append(producer)
                film.get_distributors().append(distributor)
                films_request.append(film)
    return films_request

def getNumberFilm(title):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    sparql.setQuery('SELECT ?film WHERE '
                    '{ '
                    '   ?film a dbo:Film ;'
                    '   foaf:name ?title .'
                    '   FILTER(?title = "' + title + '"@en).'
                    '}'
                    'ORDER BY(?film)')

    sparql.setReturnFormat(JSON)
    results = sparql.queryAndConvert()

    return len(results["results"]['bindings'])

def getYearFilms(title):
    years = []
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    sparql.setQuery('SELECT ?film WHERE '
                    '{ '
                    '   ?film a dbo:Film ;'
                    '   foaf:name ?title .'
                    '   FILTER(?title = "' + title + '"@en).'
                    '}'
                    'ORDER BY(?film)')

    sparql.setReturnFormat(JSON)
    results = sparql.queryAndConvert()

    for r in results["results"]['bindings'] :
        title_tmp = title.replace(" ", "_")
        years.append(r["film"]["value"].split(title_tmp)[1].split('(')[1].split("_")[0])

    return years


def getDirectorsByFilm(title, list_films):
    directors = {'year_film' : [],'title' : [], "director" : []}
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    sparql.setQuery('SELECT ?film ?title ?director WHERE '
                    '{ '
                    '   ?film a dbo:Film ;'
                    '   foaf:name ?title ;'
                    '   dbo:director ?d .'
                    '   ?d foaf:name ?director .'
                    '   FILTER(?title = "' + title + '"@en).'
                    '}'
                    'ORDER BY(?film)')

    sparql.setReturnFormat(JSON)
    results = sparql.queryAndConvert()

    for r in results["results"]['bindings']:
        if list_films > 1 :
            title_tmp = title.replace(" ", "_")
            directors["year_film"].append(r["film"]["value"].split(title_tmp)[1].split('(')[1].split("_")[0])
        directors['title'].append(r['title']['value'])
        directors['director'].append(r['director']['value'])

    return directors

def getActorsByFilm(title, list_films) :
    actors = {'year_film' : [],'title' : [], "actor" : []}
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    sparql.setQuery('SELECT ?film ?title ?actor WHERE '
                    '{ '
                    '   ?film a dbo:Film;'
                    '   foaf:name ?title;'
                    '   dbo:starring ?a .'
                    '   ?a foaf:name ?actor.'
                    '   FILTER(?title = "' + title + '" @en).'
                    '}'
                    'ORDER BY(?film)')

    sparql.setReturnFormat(JSON)
    results = sparql.queryAndConvert()

    for r in results["results"]['bindings'] :
        if list_films > 1 :
            title_tmp = title.replace(" ", "_")
            actors["year_film"].append(r["film"]["value"].split(title_tmp)[1].split('(')[1].split("_")[0])
        actors['title'].append(r['title']['value'])
        actors['actor'].append(r['actor']['value'])

    return actors

def getProducersByFilm(title, list_films) :
    producers = {'year_film' : [],'title' : [], "producer" : []}
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    sparql.setQuery('SELECT ?film ?title ?producer WHERE '
                    '{ '
                    '   ?film a dbo:Film;'
                    '   foaf:name ?title;'
                    '   dbo:producer ?p.'
                    '   ?p foaf:name ?producer.'
                    '   FILTER(?title = "'+title+'" @en).'
                    '}'
                    'ORDER BY(?film)')

    sparql.setReturnFormat(JSON)
    results = sparql.queryAndConvert()

    for r in results["results"]['bindings'] :
        if list_films > 1 :
            title_tmp = title.replace(" ", "_")
            producers["year_film"].append(r["film"]["value"].split(title_tmp)[1].split('(')[1].split("_")[0])
        producers['title'].append(r['title']['value'])
        producers['producer'].append(r['producer']['value'])

    return producers

def getDistributorByFilm(title, list_films):
    distributors = {'year_film' : [], 'title' : [], "distributor" : []}
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    sparql.setQuery('SELECT ?film ?title ?distributor WHERE '
                    '{ '
                    '   ?film a dbo:Film;'
                    '   foaf:name ?title;'
                    '   dbo:distributor ?d.'
                    '   ?d foaf:name ?distributor.'
                    '   FILTER(?title = "' + title + '" @en).'
                    '}'
                    'ORDER BY(?film)')

    sparql.setReturnFormat(JSON)
    results = sparql.queryAndConvert()

    for r in results["results"]['bindings'] :
        if list_films > 1 :
            title_tmp = title.replace(" ", "_")
            distributors["year_film"].append(r["film"]["value"].split(title_tmp)[1].split('(')[1].split("_")[0])
        distributors['title'].append(r['title']['value'])
        distributors['distributor'].append(r['distributor']['value'])

    return distributors

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)