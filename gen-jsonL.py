import json

from app.db import  get_categories, get_random_half_mercaderia_names_and_categories

mercaderias = get_random_half_mercaderia_names_and_categories()


categories = get_categories()
categories_text = "\n".join([f"({category['idcategoria']}, {category['categorianombre']})" for category in categories])

arrayEntrenamiento = []

for mercaderia in mercaderias:
    print(f"Mercaderia: {mercaderia}")
    text1 = f"""segun estas categorias:
        {categories_text}
        que categoria tiene la mercaderia : {mercaderia.get('mercaderia_nombre')}"""
    text2 = f"{{'idcategoria': {mercaderia.get('idcategoria')}, 'categoria_nombre': '{mercaderia.get('categoria_nombre')}'}}"
    arrayEntrenamiento.append({"contents": [{"role": "user", "parts": [{"text": text1}]}, {"role": "model", "parts": [{"text": text2}]}]})

with open('output.jsonl', 'w') as jsonl_file:
    for entry in arrayEntrenamiento:
        jsonl_file.write(json.dumps(entry) + '\n')

