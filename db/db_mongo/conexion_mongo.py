from pymongo import MongoClient

ATLAS: str = "mongodb+srv://root:root@clusterprueba.rsztyiu.mongodb.net/?retryWrites=true&w=majority"

db_cliente = MongoClient(ATLAS)