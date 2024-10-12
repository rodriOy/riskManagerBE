from app.db import get_mercaderia_names_and_categories
from app.generative import clasify

mercaderias = get_mercaderia_names_and_categories()
print(f"Se encontraron {len(mercaderias)} mercaderias.")

contador = contadorincorrectas = contadorcorrectas = 0
for mercaderia in mercaderias:
    contador += 1
    print(f"Mercaderia: {mercaderia.get('mercaderia_nombre')}")
    print(f"Categoria: {mercaderia.get('idcategoria')}")
    categoriaacomparar = clasify(mercaderia.get('mercaderia_nombre'))
    if int(categoriaacomparar.get('idcategoria')) == int(mercaderia.get('idcategoria')):
        print(f"Mercaderia {mercaderia.get('mercaderia_nombre')} clasificada correctamente.")
        contadorcorrectas += 1
    else:
        print(f"Mercaderia {mercaderia.get('mercaderia_nombre')} clasificada incorrectamente.")
        contadorincorrectas += 1
    print(f"Progreso: {contador}/{len(mercaderias)} mercaderias procesadas.")
print(f"Se clasificaron {contador} mercaderias, de las cuales {contadorcorrectas} fueron clasificadas correctamente y {contadorincorrectas} incorrectamente.")
