from flask import Blueprint, request, jsonify
from app.utils import detect_language, preprocess_text, get_predictions
from app.db import load_data_from_db, associate_section_with_category, get_sections, get_categories, \
    get_security_measures, associate_section_with_security_measure, get_mercaderia_details
import logging

bp = Blueprint('routes', __name__)
data = load_data_from_db()
texts = [row[1] for row in data]
ids = [row[0] for row in data]
categories = [row[2] for row in data]


@bp.route('/predict', methods=['POST'])
def predict():
    input_text = request.json.get('text')
    language = detect_language(input_text)
    logging.debug(f"Idioma detectado: {language}")
    processed_input = preprocess_text(input_text, language)
    predictions = get_predictions(processed_input, texts, ids)
    logging.debug(f"Predicciones: {predictions}")
    return jsonify(predictions)


@bp.route('/submit', methods=['POST'])
def submit():
    mercaderia_id = request.form.get('mercaderiaId')
    valor = request.form.get('valor')
    logging.debug(f"Mercadería ID: {mercaderia_id}, Valor: {valor}")
    return jsonify({"message": "Formulario enviado.", "mercaderiaId": mercaderia_id, "valor": valor})


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


@bp.route('/categorias', methods=['GET'])
def categorias():
    try:
        categories = get_categories()
        return jsonify(categories), 200
    except Exception as e:
        logging.error(f"Error al obtener categorías: {e}")
        return jsonify({"error": str(e)}), 500


@bp.route('/secciones', methods=['GET'])
def secciones():
    try:
        sections = get_sections()
        return jsonify(sections), 200
    except Exception as e:
        logging.error(f"Error al obtener secciones: {e}")
        return jsonify({"error": str(e)}), 500


@bp.route('/medidas', methods=['GET'])
def medidas():
    try:
        measures = get_security_measures()
        return jsonify(measures), 200
    except Exception as e:
        logging.error(f"Error al obtener medidas de seguridad: {e}")
        return jsonify({"error": str(e)}), 500


@bp.route('/associate_seccion_medida', methods=['POST'])
def associate_seccion_medida():
    seccion_id = request.json.get('seccion_id')
    medida_id = request.json.get('medida_id')

    if not seccion_id or not medida_id:
        return jsonify({"error": "Se requiere seccion_id y medida_id"}), 400

    try:
        associate_section_with_security_measure(seccion_id, medida_id)
        return jsonify({"message": "Asociación completada."}), 200
    except Exception as e:
        logging.error(f"Error al asociar: {e}")
        return jsonify({"error": str(e)}), 500


@bp.route('/mercaderia/<int:mercaderia_id>', methods=['GET'])
def mercaderia_details(mercaderia_id):
    try:
        details = get_mercaderia_details(mercaderia_id)
        if details:
            return jsonify(details), 200
        else:
            return jsonify({"error": "Mercaderia no encontrada"}), 404
    except Exception as e:
        logging.error(f"Error al obtener detalles de mercaderia: {e}")
        return jsonify({"error": str(e)}), 500
