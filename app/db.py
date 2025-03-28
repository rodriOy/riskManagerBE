from db_connection import get_connection


def associate_section_with_category(seccion_id, categoria_id):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        query = "UPDATE categoria SET seccion_id = %s WHERE idcategoria = %s"
        cursor.execute(query, (seccion_id, categoria_id))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()


def get_categories():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT idcategoria, categorianombre, seccion_id FROM categoria")
    categories = cursor.fetchall()
    cursor.close()
    connection.close()
    return [{"idcategoria": row[0], "categorianombre": row[1], "seccion_id": row[2]} for row in categories]


def create_category(categorianombre):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        query = "INSERT INTO categoria (categorianombre) VALUES (%s)"
        cursor.execute(query, (categorianombre,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()


def get_sections():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT seccion_id, seccion_nombre FROM seccion")
    sections = cursor.fetchall()
    cursor.close()
    connection.close()
    return [{"seccion_id": row[0], "seccion_nombre": row[1]} for row in sections]


def create_section(seccion_nombre):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        query = "INSERT INTO seccion (seccion_nombre) VALUES (%s)"
        cursor.execute(query, (seccion_nombre,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()


def get_security_measures():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT idmedidasseguridad, medida FROM medidasseguridad")
    measures = cursor.fetchall()
    cursor.close()
    connection.close()
    return [{"idmedidasseguridad": row[0], "medida": row[1]} for row in measures]


def create_security_measure(medida_nueva):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        query = "INSERT INTO medidasseguridad (medida) VALUES (%s)"
        cursor.execute(query, (medida_nueva,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()


def associate_section_with_security_measure(seccion_id, medida_id, cotainf, cotasup):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        query = "INSERT INTO seccion_medidas (seccion_id, idmedidasseguridad, cotainf, cotasup) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (seccion_id, medida_id, cotainf, cotasup))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()


def get_mercaderia_details(categoria_id, sat):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        # Obtener la sección asociada a la mercadería
        query = ("SELECT s.seccion_id, s.seccion_nombre FROM  categoria c "
                 " JOIN seccion s ON c.seccion_id = s.seccion_id WHERE c.idcategoria = %s")
        cursor.execute(query, (categoria_id,))
        seccion = cursor.fetchone()

        if not seccion:
            return None

        seccion_id, seccion_nombre = seccion

        if seccion_id == 1 and sat < 150001:
            return {
                "seccion_id": seccion_id,
                "seccion_nombre": seccion_nombre,
                "medidas": [{"idmedidasseguridad": 0, "medida": "No requiere medidas de seguridad", "cotainf": 0,
                             "cotasup": 150000}]
            }
        else:
            # Obtener las medidas de seguridad asociadas a la sección
            query = (
                "SELECT ms.idmedidasseguridad, ms.medida, sm.cotainf, sm.cotasup FROM seccion_medidas sm JOIN "
                "medidasseguridad ms ON sm.idmedidasseguridad = ms.idmedidasseguridad WHERE sm.seccion_id = %s AND "
                "sm.cotainf <= %s AND sm.cotasup >= %s")
            cursor.execute(query, (seccion_id, sat, sat))
            medidas = cursor.fetchall()

        return {
            "seccion_id": seccion_id,
            "seccion_nombre": seccion_nombre,
            "medidas": [{"idmedidasseguridad": row[0], "medida": row[1], "cotainf": row[2], "cotasup": row[3]} for row
                        in medidas]
        }
    finally:
        cursor.close()
        connection.close()

def get_mercaderia_names_and_categories():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        query = "SELECT mercaderianombre, idcategoria FROM mercaderia GROUP BY mercaderianombre, idcategoria"
        cursor.execute(query)
        mercaderia = cursor.fetchall()
        return [{"mercaderia_nombre": row[0], "idcategoria": row[1]} for row in mercaderia]
    finally:
        cursor.close()
        connection.close()

def get_random_half_mercaderia_names_and_categories():
    import random
    connection = get_connection()
    cursor = connection.cursor()
    try:
        query = ("SELECT mercaderianombre, categoria.idcategoria, categoria.categorianombre FROM mercaderia "
                 "join categoria on mercaderia.idcategoria = categoria.idcategoria GROUP BY mercaderianombre, idcategoria")
        cursor.execute(query)
        mercaderia = cursor.fetchall()
        half_size = len(mercaderia) // 2
        random_mercaderia = random.sample(mercaderia, half_size)
        return [{"mercaderia_nombre": row[0], "idcategoria": row[1], "categoria_nombre": row[2] } for row in random_mercaderia]
    finally:
        cursor.close()
        connection.close()
