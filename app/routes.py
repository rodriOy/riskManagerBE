from flask import Blueprint, request, jsonify
from app.utils import detect_language, preprocess_text, get_predictions
from app.db import load_data_from_db
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
