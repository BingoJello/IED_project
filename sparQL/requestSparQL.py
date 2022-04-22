from SPARQLWrapper import SPARQLWrapper, JSON, XML
import json
import xml.etree.ElementTree as ET

def selectQuery():
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    sparql.setQuery("""
        SELECT ?an ?y ?p WHERE { 
            ?f a dbo:Film ;
            foaf:name "Ed Wood"@en ;
            dbo:starring ?a .
            ?a foaf:name ?an ;
            dbo:birthYear ?y ;
            dbo:birthPlace ?p.
            } 
    """)

    sparql.setReturnFormat(JSON)
    results = sparql.queryAndConvert()
    for r in results["results"]['bindings']:
        print(r['an']['value'])
        print(r['y']['value'])
        print(r['p']['value'])