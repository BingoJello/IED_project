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

    return request_films

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