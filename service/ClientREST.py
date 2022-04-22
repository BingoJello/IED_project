import requests
import xml.etree.ElementTree as ET
from lxml import etree
from xml.dom import minidom
from xml.dom.minidom import parse


def getRequest():
    response = requests.get("http://www.omdbapi.com/?r=xml&i=tt3896198&apikey=a834ebc0")
    #dom = minidom.parseString(response.content)
    #name_element = dom.getElementsByTagName("movie")[0]
    tree = etree.parse(response.)
    for film in tree.xpath("/movie/title/") :
        print(user.text)