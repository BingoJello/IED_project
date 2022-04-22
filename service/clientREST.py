import requests

def getRequest():
    response = requests.get("http://www.omdbapi.com/?i=tt3896198&apikey=a834ebc0")

    print(response.json())  # This method is convenient when the API returns JSON
