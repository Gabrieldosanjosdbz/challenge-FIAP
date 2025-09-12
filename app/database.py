import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# conexão
client = MongoClient(os.getenv("MONGO_URL"))

# criando database
db = client["challenge_db"]

# criando collection
collection = db["relatorio"]