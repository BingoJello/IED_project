import mysql.connector
from model.Film import Film

def get_co():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="A123456*",
        database="ied"
    )
    return mydb

def selectQuery(title):
    films = []
    db = get_co()
    mycursor = db.cursor()

    query = 'SELECT * FROM movie where name = "'+title+'"'

    mycursor.execute(query)

    myresult = mycursor.fetchall()
    for row in myresult :
        film = Film()
        film.set_id(row[0])
        film.set_release_date(row[1])
        film.set_name(row[2])
        film.set_production_budget(row[3])
        film.set_domestic_gross(row[4])
        film.set_worldwide_gross(row[5])
        film.set_distributor(row[6])
        film.set_genre(row[7])

        films.append(film)

    return films
