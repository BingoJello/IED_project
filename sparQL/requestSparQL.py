from SPARQLWrapper import SPARQLWrapper, JSON, XML
import json
import xml.etree.ElementTree as ET


def getListFilm(title):
    directors = {'year' : [], "directors":[]}
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    sparql.setQuery('SELECT ?film WHERE '
                    '{ '
                    '   ?film a dbo:Film ;'
                    '   foaf:name ?title ;'
                    '   FILTER(?title = "' + title + '"@en).'
                    '}'
                    'ORDER BY(?film)')

    sparql.setReturnFormat(JSON)
    results = sparql.queryAndConvert()

    return len(results["results"]['bindings']);


def getDirectors(title):
    directors = {'year' : [], "directors":[]}
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
    list_films = getListFilm(title)
    for r in results["results"]['bindings']:
        if(list_films > 1):
            directors["year"] = r["film"]["value"].split(title)[1].split('(')[1].split("_")[0]
        # directos[]
        #directors.append(r['film']['value'])
    exit(0)
    return directors

def getActors(title) :
    actors = []
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    sparql.setQuery('SELECT ?f ?t ?actor WHERE '
                    '{ '
                    '   ?f a dbo: Film;'
                    '   foaf: name ?t;'
                    '   dbo:starring ?a .'
                    '   ?a foaf:name ?actor.'
                    '   FILTER(?t = "' + title + '" @ en).'
                    '}'
                    'ORDER BY(?f)')

    sparql.setReturnFormat(JSON)
    results = sparql.queryAndConvert()

    for r in results["results"]['bindings'] :
        actors.append(r['actor']['value'])

    return actors

def getProducers(title) :
    producers = []
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery('SELECT ?f ?t ?producer WHERE '
                    '{ '
                    '   ?f a dbo: Film;'
                    '   foaf: name ?t;'
                    '   dbo: producer ?p.'
                    '   ?p foaf: name ?producer.'
                    '   FILTER(?t = "'+title+'" @ en).'
                    '}'
                    'ORDER BY(?f)')

    sparql.setReturnFormat(JSON)
    results = sparql.queryAndConvert()

    for r in results["results"]['bindings'] :
        producers.append(r['producer']['value'])

    return producers