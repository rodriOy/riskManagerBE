from db_connection import get_connection

def load_data_from_db():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT idmercaderia, mercaderianombre, idcategoria FROM mercaderia limit 20000")
    mercaderia = cursor.fetchall()
    cursor.close()
    connection.close()
    return mercaderia
