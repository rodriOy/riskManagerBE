from db_connection import get_connection


def load_data_from_db():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT idmercaderia, mercaderianombre, idcategoria FROM mercaderia limit 20000")
    mercaderia = cursor.fetchall()
    cursor.close()
    connection.close()
    return mercaderia


def associate_section_with_category(seccion_id, categoria_id):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("UPDATE categoria SET seccion_id = ? WHERE idcategoria = ?", (seccion_id, categoria_id))
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
        #cursor.execute("INSERT INTO seccion_medidas (seccion_id, idmedidasseguridad, cotainf, cotasup) VALUES (?, ?, "
        #               "?, ?)", (seccion_id, medida_id, cotainf, cotasup))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()


def get_mercaderia_details(mercaderia_id, sat):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        # Obtener la sección asociada a la mercadería
        cursor.execute(
            "SELECT s.seccion_id, s.seccion_nombre FROM mercaderia m JOIN categoria c ON m.idcategoria = c.idcategoria "
            "JOIN seccion s ON c.seccion_id = s.seccion_id WHERE m.idmercaderia = ?",
            (mercaderia_id,))
        seccion = cursor.fetchone()

        if not seccion:
            return None

        seccion_id, seccion_nombre = seccion

        # Obtener las medidas de seguridad asociadas a la sección
        cursor.execute(
            "SELECT ms.idmedidasseguridad, ms.medida, sm.cotainf, sm.cotasup FROM seccion_medidas sm "
            "JOIN medidasseguridad ms ON sm.idmedidasseguridad = ms.idmedidasseguridad WHERE sm.seccion_id = ? AND "
            "sm.cotainf <= ? AND sm.cotasup >= ?",
            (seccion_id, sat, sat))
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
