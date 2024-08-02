import os
from dotenv import load_dotenv
import pymysql as mysql


# Cargar variables de entorno desde el archivo .env
load_dotenv()


def get_connection():
    try:
        connection = mysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME")
        )
        return connection
    except mysql.Error as err:
        print(f"Error al conectar la DB: {err}")
        return None
