import requests
import xml.etree.ElementTree as ET
from lxml import etree
from xml.dom import minidom
from xml.dom.minidom import parse


def getRequest():
    response = requests.get("http://www.omdbapi.com/?r=xml&i=tt3896198&apikey=a834ebc0&title=Harry")
    root = ET.fromstring(response.content)

    for elem in root.findall('.//movie') :
        # How to make decisions based on attributes even in 2.6:
        print(elem.attrib.get('plot'))


