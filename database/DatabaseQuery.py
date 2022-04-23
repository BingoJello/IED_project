import mysql.connector
from model.Film import Film

def get_co():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        # password="A123456*",
        password="",
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
    for row in myresult:
        film = Film(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        films.append(film)
    return films
