import Mediator
from tkinter import *


def film_command():
    result.delete('1.0', END)
    title_film = input_film.get()
    request_films = Mediator.getInfoByFilm(title_film)
    text = printFilmByTitle(request_films)

    result.insert(END, text)

def actor_command():
    result.delete('1.0', END)
    actor_name = input_actor.get()
    request_films = Mediator.getInfoByActor(actor_name)
    text = printFilmByActor(request_films)

    result.insert(END, text)

def printFilmByTitle(films):
    separator = ", "
    text = ""
    i = 1

    if len(films) <= 0:
        text = "Aucun résultat"
        return text

    for film in films:
        text = text+"---------- FILM "+str(i)+" ----------:\n"

        if film.get_name() != "" :
            title = film.get_name()
        else:
            title = "Inconnue"

        text = text+"Titre : "+title+"\n"

        if film.get_release_date() != "":
            parution = film.get_release_date()
        elif film.get_year() != "" :
            parution = film.get_year()
        else:
            parution = "Inconnue"

        text = text+"Date de sortie : "+parution+ "\n"

        if film.get_genre() != "":
            genre = film.get_genre()
        else:
            genre = "Inconnue"

        text = text + "Genre : " + genre+ "\n"

        film.get_distributors()

        if len(film.get_distributors()) > 0:
            distributor = separator.join(film.get_distributors())
        else :
            distributor = "Inconnue"

        text = text + " Distributeur : " + distributor+ "\n"

        if film.get_production_budget() != "" :
            production_budget = film.get_production_budget()
        else :
            production_budget = "Inconnue"

        text = text+" Budget de production : "+production_budget+"\n"

        if film.get_domestic_gross() != "" :
            domestic_gross = film.get_domestic_gross()
        else :
            domestic_gross = "Inconnue"

        text = text + " Revenus aux Etats Unis : " + domestic_gross + "\n"

        if film.get_worldwide_gross() != "" :
            worldwide_gross = film.get_worldwide_gross()
        else :
            worldwide_gross = "Inconnue"

        text = text + " Revenus mondiaux : " + worldwide_gross+ "\n"


        if len(film.get_directors()) > 0 :
            directors = separator.join(film.get_directors())
        else :
            directors = "Inconnue"

        text = text + " Réalisateurs : " + directors+ "\n"

        if len(film.get_actors()) > 0 :
            actors = separator.join(film.get_actors())
        else :
            actors = "Inconnue"

        text = text + " Acteurs : " + actors + "\n"

        if len(film.get_producers()) > 0 :
            producers = separator.join(film.get_producers())
        else :
            producers = "Inconnue"

        text = text + " Producteurs : " + producers + "\n"

        if film.get_plot() != "" :
            plot = film.get_plot()
        else :
            plot = "Inconnue"

        text = text + " Résumé : " + plot + "\n"
        i+=1
        text = text+"\n"
    return text

def printFilmByActor(films):
    separator = ", "
    text = ""
    i = 1

    if len(films) <= 0:
        text = "Aucun résultat"
        return text

    for film in films:
        text = text+"---------- FILM "+str(i)+" ----------:\n"

        if film.get_name() != "" :
            title = film.get_name()
        else:
            title = "Inconnue"

        text = text+"Titre : "+title+"\n"

        if film.get_release_date() != "":
            parution = film.get_release_date()
        elif film.get_year() != "" :
            parution = film.get_year()
        else:
            parution = "Inconnue"

        text = text+"Date de sortie : "+parution+ "\n"

        if film.get_genre() != "":
            genre = film.get_genre()
        else:
            genre = "Inconnue"

        text = text + "Genre : " + genre+ "\n"

        print("----------------")
        film.get_distributors()

        if len(film.get_distributors()) > 0:
            distributor = separator.join(film.get_distributors())
        else :
            distributor = "Inconnue"

        text = text + " Distributeur : " + distributor+ "\n"

        if len(film.get_directors()) > 0 :
            directors = separator.join(film.get_directors())
        else :
            directors = "Inconnue"

        text = text + " Réalisateurs : " + directors+ "\n"

        if len(film.get_producers()) > 0 :
            producers = separator.join(film.get_producers())
        else :
            producers = "Inconnue"

        text = text + " Producteurs : " + producers + "\n"

        i+=1
        text = text+"\n"
    return text


window = Tk()
window.title("Projet IED")
window.geometry("1200x600")
label_title = Label(window, text="Projet IED", font=("Arial", 20))

label_title.pack(pady=10)
input_film = Entry(window, width=40)
input_film.pack(pady=10)
placeholder = "Recherche film"
input_film.insert(0, placeholder)

Button(window, text="Recherche", command=film_command).pack()

input_actor = Entry(window, width=40)
input_actor.pack(pady=10)
placeholder = "Recherche acteur"
input_actor.insert(0, placeholder)

Button(window, text="Recherche", command=actor_command).pack()

result = Text(window, height=40, width=130)
result.pack(pady=10)
window.mainloop()