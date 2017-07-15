from lxml import html
import requests
import csv
import random

cookies = {
    '__utmt': '1',
    '__utma': '17573176.466661072.1498867554.1498867554.1498870955.2',
    '__utmb': '17573176.41.10.1498870955',
    '__utmc': '17573176',
    '__utmz': '17573176.1498867554.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
}

headers = {
    'Origin': 'http://www.peseu.com',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'es-ES,es;q=0.8,en;q=0.6',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Referer': 'http://www.peseu.com/puntajes-psu-a%C3%B1os-anteriores/',
    'Connection': 'keep-alive',
}

def get_puntajes_2015(datos):
    """ 
    get_puntajes_2015: metodo para obtener los puntajes de una persona
    de la admision 2015. Recibe una tupla con los datos de la persona en el 
    orden (nombres, apellido paterno, apellido materno)
    """
    data = [
        ('tipo', 'nombre'),
        ('nombres', datos[0]),
        ('paterno', datos[1]),
        ('materno', datos[2]),
        ('admision', '2015'),
    ]

    pagina = requests.post(
        'http://www.peseu.com/busqueda', headers=headers, cookies=cookies, data=data)
    # Puntajes de la persona
    tree_puntajes = html.fromstring(pagina.content)
    puntajes_personas = tree_puntajes.xpath('//table/tr/td/text()')[2:]

    return puntajes_personas

def obtener_tupla_nombre(nombre_entero):
    """
    obtener_tupla_nombre: metodo para transformar de un solo string con 
    el nombre entero a una tupla para recibir los puntajes.
    Retorna una tupla del estilo (nombres, apellido paterno, apellido materno)
    """
    nombre_aux = nombre_entero.split(' ')
    if len(nombre_aux) == 5:
        nombre = '{} {} {}'.format(nombre_aux[0], nombre_aux[1], nombre_aux[2])
        apellido_paterno = nombre_aux[3]
        apellido_materno = nombre_aux[4]
        # Tupla retornada
        tupla = (nombre, apellido_paterno, apellido_materno)
        return tupla
    
    elif len(nombre_aux) == 4:
        nombre = '{} {}'.format(nombre_aux[0], nombre_aux[1])
        apellido_paterno = nombre_aux[2]
        apellido_materno = nombre_aux[3]
        # Tupla retornada
        tupla = (nombre, apellido_paterno, apellido_materno)
        return tupla

    elif len(nombre_aux) == 3:
        nombre = nombre_aux[0]
        apellido_paterno = nombre_aux[1]
        apellido_materno = nombre_aux[2]
        # Tupla retornada
        tupla = (nombre, apellido_paterno, apellido_materno)
        return tupla

    else:
        return None


if __name__ == "__main__":
    tupla = obtener_tupla_nombre('ISIDORA CONSTANZA CAROLIN MOREIRA GOMEZ')
    print(get_puntajes_2015(tupla))