from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de la conexión a MongoDB
DATABASE_URL = os.getenv("MONGODB_URL_CONNECTION")




client = MongoClient(DATABASE_URL)

# Selecciona la base de datos que usarás
db = client["multidisciplinario"]  # Aquí se usa "codebox" como el nombre de la base de datos

# Opcionalmente, puedes seleccionar las colecciones de la base de datos
personajes_collection = db["personaje"]
paredes_collection = db["pared"]
puentes_collection = db["puente"]
terminales_collection = db["terminal"]
bloques_codigo_collection = db["bloqueCodigo"]
terminales_codigo_collection = db["terminalCodigo"]
