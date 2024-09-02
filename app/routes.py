from flask import Blueprint, request, jsonify
from flask_cors import CORS
from app.db import associate_section_with_category, get_sections, get_categories, \
    get_security_measures, associate_section_with_security_measure, get_mercaderia_details, create_category, \
    create_section, create_security_measure
import logging

from app.generative import clasify

bp = Blueprint('routes', __name__)
CORS(bp)


@bp.route('/generate', methods=['GET'])
def generate_route():
    mercaderia = request.json.get('mercaderia')

    if not mercaderia:
        return jsonify({"error": "Se requiere mercaderia"}), 400

    try:
        categoria = clasify(mercaderia)
        print(categoria)
        return categoria, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ep para asociar categoria con seccion
@bp.route('/associate', methods=['POST'])
def associate():
    seccion_id = request.json.get('seccion_id')
    categoria_id = request.json.get('categoria_id')

    if not seccion_id or not categoria_id:
        return jsonify({"error": "Se requiere seccion_id y categoria_id"}), 400

    try:
        associate_section_with_category(seccion_id, categoria_id)
        return jsonify({"message": "Asociación completada."}), 200
    except Exception as e:
        logging.error(f"Error al asociar: {e}")
        return jsonify({"error": str(e)}), 500


# ep para obtener categorias
@bp.route('/categorias', methods=['GET'])
def categorias():
    try:
        categories = get_categories()
        return jsonify(categories), 200
    except Exception as e:
        logging.error(f"Error al obtener categorías: {e}")
        return jsonify({"error": str(e)}), 500


# ep para crear categoria
@bp.route('/categorias', methods=['POST'])
def create_categoria():
    categorianombre = request.json.get('categorianombre')

    if not categorianombre:
        return jsonify({"error": "Se requiere categorianombre"}), 400

    try:
        create_category(categorianombre)
        return jsonify({"message": "Categoría creada exitosamente."}), 201
    except Exception as e:
        logging.error(f"Error al crear categoría: {e}")
        return jsonify({"error": str(e)}), 500


# ep para obtener secciones
@bp.route('/secciones', methods=['GET'])
def secciones():
    try:
        sections = get_sections()
        return jsonify(sections), 200
    except Exception as e:
        logging.error(f"Error al obtener secciones: {e}")
        return jsonify({"error": str(e)}), 500


# ep para crear seccion
@bp.route('/secciones', methods=['POST'])
def create_seccion():
    seccion_nombre = request.json.get('seccion_nombre')

    if not seccion_nombre:
        return jsonify({"error": "Se requiere seccion_nombre"}), 400

    try:
        create_section(seccion_nombre)
        return jsonify({"message": "Sección creada exitosamente."}), 201
    except Exception as e:
        logging.error(f"Error al crear sección: {e}")
        return jsonify({"error": str(e)}), 500


# ep para obtener medidas de seguridad
@bp.route('/medidas', methods=['GET'])
def medidas():
    try:
        measures = get_security_measures()
        return jsonify(measures), 200
    except Exception as e:
        logging.error(f"Error al obtener medidas de seguridad: {e}")
        return jsonify({"error": str(e)}), 500


# ep para crear medida de seguridad
@bp.route('/medidas', methods=['POST'])
def create_medida():
    medida = request.json.get('medida')

    if not medida:
        return jsonify({"error": "Se requiere medida"}), 400

    try:
        create_security_measure(medida)
        return jsonify({"message": "Medida de seguridad creada exitosamente."}), 201
    except Exception as e:
        logging.error(f"Error al crear medida de seguridad: {e}")
        return jsonify({"error": str(e)}), 500


# ep para asociar seccion con medida de seguridad
@bp.route('/associate_seccion_medida', methods=['POST'])
def associate_seccion_medida():
    seccion_id = request.json.get('seccion_id')
    medida_id = request.json.get('medida_id')
    cotainf = request.json.get('cotainf')
    cotasup = request.json.get('cotasup')

    if not seccion_id or not medida_id or cotainf is None or cotasup is None:
        return jsonify({"error": "Se requiere seccion_id, medida_id, cotainf y cotasup"}), 400

    try:
        associate_section_with_security_measure(seccion_id, medida_id, cotainf, cotasup)
        return jsonify({"message": "Asociación completada."}), 200
    except Exception as e:
        logging.error(f"Error al asociar: {e}")
        return jsonify({"error": str(e)}), 500


# ep para obtener detalles de las medidas de seguridad segun Suma asegurada total y mercaderia
@bp.route('/mercaderia', methods=['GET'])
def mercaderia_details():
    SAT = request.args.get('SAT', type=int)
    mercaderia = request.args.get('mercaderia', type=str)
    try:
        categoria = clasify(mercaderia)
        idcategoria = categoria.get('idcategoria')
        details = get_mercaderia_details(idcategoria, SAT)
        if details:
            return jsonify(details), 200
        else:
            return jsonify({"error": "Mercaderia no encontrada"}), 404
    except Exception as e:
        logging.error(f"Error al obtener detalles de mercaderia: {e}")
        return jsonify({"error": str(e)}), 500
