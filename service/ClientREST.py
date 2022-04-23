import requests
import xml.etree.ElementTree as ET
from model.Film import Film
from lxml import etree
from xml.dom import minidom
from xml.dom.minidom import parse


def getRequest(title):
    url = "http://www.omdbapi.com/?r=xml&i=tt3896198&apikey=a834ebc0&t="+title
    response = requests.get(url)

    root = ET.fromstring(response.content)
    film = []
    for elem in root.findall('.//movie') :
        # How to make decisions based on attributes even in 2.6:
        film = Film()
        film.set_name(elem.attrib.get("title"))
        film.set_year(elem.attrib.get("year"))
        film.add_director(elem.attrib.get("director"))
        film.set_actors(elem.attrib.get("actors"))
        return film


