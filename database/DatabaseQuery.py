import DatabaseConnection as dc

def selectQuery(query):
    db = dc.get_co()
    mycursor = db.cursor()

    query = ""

    mycursor.execute(query)

    myresult = mycursor.fetchall()
