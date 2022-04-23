from sparQL import requestSparQL as spark
from service import ClientREST
from database import DatabaseQuery

spark.getActors("Godzilla")
# ClientREST.getRequest("Godzilla")
# DatabaseQuery.selectQuery("Avatar")
