import requests
import xml.etree.ElementTree as ET
from model.Film import Film


def getRequest(films, title = False):
    if title == False and len(films) <= 0:
        return []

    films_request = []

    if len(films) > 1 :
        for film in films:
            genre = False
            directors = False
            actors = False
            year = False

            if film.get_year() != "":
                year = film.get_year()
            elif film.get_release_date() != "":
                year = film.get_release_date().split("/")[2]
            if film.get_genre() == "":
                genre = True
            if len(film.get_directors()) <= 0:
                directors = True
            if len(film.get_actors()) <= 0:
                actors = True
            if title == False:
                title = film.get_name().replace(" ", "_")
            film_response = getResponseByFilm(title, year, genre, directors, actors)

            if film_response is not None :
                if film_response['plot'] != "":
                    film.set_plot(film_response['plot'])
                if len(film_response['directors']) > 0 and len(film.get_directors()) <= 0:
                    film.get_directors().extend(film_response['directors'])
                if len(film_response['actors']) > 0 and len(film.get_actors()) <= 0:
                    film.get_actors().extend(film_response['actors'])
                if film_response['genre'] != "" and film.get_genre() == "":
                    film.set_genre(film_response['genre'])
                if film_response['year'] != "" and film.get_release_date() == "":
                    film.set_release_date(film_response['year'])

            films_request.append(film)
            title = False
    else:
        year = False
        if len(films) > 0:
            film = films[0]
        else:
            film = Film()
            film.set_name(title)

        genre = False
        directors = False
        actors = False

        if film.get_release_date() != "":
            year = film.get_release_date().split("/")[2]
        if film.get_genre() == "" :
            genre = True
        if len(film.get_directors()) <= 0 :
            directors = True
        if len(film.get_actors()) <= 0 :
            actors = True
        if title == False :
            title = film.get_name().replace(" ", "_")

        film_response = getResponseByFilm(title, year, genre, directors, actors)

        if film_response is None :
            return films_request

        if film_response['plot'] != "" :
            film.set_plot(film_response['plot'])
        if len(film_response['directors']) > 0 and len(film.get_directors()) <= 0 :
            film.get_directors().extend(film_response['directors'])
        if len(film_response['actors']) > 0 and len(film.get_actors()) <= 0 :
            film.get_actors().extend(film_response['actors'])
        if film_response['genre'] != "" and film.get_genre() == "" :
            film.set_genre(film_response['genre'])
        if film_response['year'] != "" and film.get_release_date() == "" :
            film.set_release_date(film_response['year'])

        films_request.append(film)
        title = False
    return films_request

def getResponseByFilm(title, year, genre, directors, actors):
    key = 'i=tt3896198&apikey=a834ebc0'
    request = "http://www.omdbapi.com/?r=xml&"+key+"&t="+title

    if year != False:
        request = request+"&y="+year

    response = requests.get(request)
    root = ET.fromstring(response.content)

    for elem in root.findall('.//movie') :
        if genre != False:
            elem_genre = elem.attrib.get('genre')
        else:
            elem_genre = ""
        if directors != False:
            elem_directors = elem.attrib.get('director').split(",")
        else:
            elem_directors = ""
        if actors != False:
            elem_actors = elem.attrib.get('actors').split(",")
        else:
            elem_actors = ""
        if year == False:
            elem_year = elem.attrib.get('released')
        else:
            elem_year = ""

        elem_plot = elem.attrib.get('plot')

        film = {'genre' : elem_genre, 'directors' : elem_directors, 'actors' : elem_actors, 'plot' : elem_plot, 'year' : elem_year}
        return film


