import json

import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting

from app.db import get_categories


def clasify(mercaderia):
    vertexai.init(project="1002854262523", location="us-central1")
    model = GenerativeModel(
        "projects/1002854262523/locations/us-central1/endpoints/7062894360437719040",
        system_instruction=[textsi_1]
    )
    text1 = f"""segun estas categorias:
    {categories_text}
    que categoria tiene la mercaderia : {mercaderia}"""

    try:
        responses = model.generate_content(
            [text1],
            generation_config=generation_config,
            safety_settings=safety_settings,
            stream=True,
        )
        full_text = ""
        for response in responses:
            full_text += response.text

        cleaned_text = full_text.replace("'", '"').strip().strip("```").strip().strip("json").strip()

        try:
            # Intentar transformar el texto completo en un JSON
            json_data = json.loads(cleaned_text)
            print("JSON generado:")
            print(json.dumps(json_data, indent=4))  # Imprimir el JSON de manera legible
        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON: {e}")
            print("Texto recibido:")
            print(full_text)
        return json_data
    except Exception as e:
        return {"error": "Error en la generación de contenido", "detalles": str(e)}


categories = get_categories()
categories_text = "\n".join([f"({category['idcategoria']}, {category['categorianombre']})" for category in categories])

textsi_1 = """Sos un clasificador de mercaderias. Dada una o mas mercaderias, tu tarea sera dar la categoria de ellas 
segun las que sean provistas. Debes responder un JSON con idcategoria y categoria. El json debe tener el siguiente formato: {"idcategoria2: , "categoria_nombre": }"""
generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_NONE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_NONE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_NONE
    ),
]
