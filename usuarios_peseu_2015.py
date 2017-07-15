from lxml import html
import requests
import csv

# Obtener la lista de universidades
pagina = requests.get('http://www.peseu.com/listas-de-seleccionados/2015/')
tree_ues = html.fromstring(pagina.content)
ues = tree_ues.xpath('//tbody/tr/td/a/text()')[::2]

# Acá se guardaran las universidades con sus carreras
universidades_con_carreras = {}

# Iterar sobre las universidades para sacar las carreras
for u in ues:
    print('[DEBUG] Obteniendo carreras de: {}'.format(u))
    pagina_carreras = requests.get(
        'http://www.peseu.com/listas-de-seleccionados/2015/{}'.format(u))
    tree_carreras = html.fromstring(pagina_carreras.content)

    nombres_carreras = tree_carreras.xpath('//table/tr/td/text()')[3::2]
    codigos_carreras = tree_carreras.xpath('//table/tr/td/a/text()')[2::2]
    links_carreras = tree_carreras.xpath('//table/tr/td/a/@href')[2::2]

    # Guardar las carreras con sus codigos en una tupla
    universidades_con_carreras[u] = list(
        zip(codigos_carreras, nombres_carreras, links_carreras))

# Datos guardados de las personas
personas_con_carreras = {}

# Cookies guardadas para hacer request
cookies = {
    '__utmt': '1',
    '__utma': '17573176.466661072.1498867554.1498867554.1498870955.2',
    '__utmb': '17573176.111.10.1498870955',
    '__utmc': '17573176',
    '__utmz': '17573176.1498867554.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
}

# Headers para hacer request
headers = {
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'es-ES,es;q=0.8,en;q=0.6',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
}


with open('usuarios_peseu_2015.csv', 'w', newline='') as file:
    escritor_csv = csv.writer(file, delimiter=',',
                              quotechar='|', quoting=csv.QUOTE_MINIMAL)
    # Iterar sobre  las universidades para conseguir carreras
    for universidad in universidades_con_carreras:
        # Iterrar sobre carreras para conseguir postulaciones
        for carrera in universidades_con_carreras[universidad]:
            print('[DEBUG] Sacando postulantes de: {}'.format(carrera))
            
            # VERSION 1.0
            # pagina_postulacion = requests.get('http://www.peseu.com/listas-de-seleccionados/2015/{}/{}'.format(
            #     universidad, carrera[1]), headers=headers, cookies=cookies)

            # VERSION 2.0
            pagina_postulacion =  requests.get('http://www.peseu.com/{}'.format(
                carrera[2]), headers=headers, cookies=cookies)

            # Guardar datos de las personas que postulan
            tree_postulacion = html.fromstring(pagina_postulacion.content)
            
            # personas_rut = tree_postulacion.xpath('//tbody/tr/td/text()')[1::5]
            columnas_personas = tree_postulacion.xpath(
                '//table/tr')[1:]

            try:
                personas_nombre = [p.xpath('td/text()')[1] for p in columnas_personas]
                personas_puntaje = [p.xpath('td/text()')[2] for p in columnas_personas]
                personas_situacion = [p.xpath('td/text()')[3] for p in columnas_personas]

                # Key que se usará para guardar todos estos datos en el diccionario
                key_a_guardar = carrera[1] + '_' + universidad
                # Guardar todos los datos obtenidos en el diccionario
                personas_con_carreras[key_a_guardar] = list(
                    zip(personas_nombre, personas_puntaje, personas_situacion))

                # Iterar en cada persona que se encontró para guardar en csv
                for persona in personas_con_carreras[key_a_guardar]:
                    escritor_csv.writerow(persona + (universidad, carrera[0]))
                
                print('[DEBUG] Cantidad de personas en: {} = {}'.format(
                    key_a_guardar, len(personas_con_carreras[key_a_guardar])))

            except Exception as e:
                print('[ERROR] Ocurrió un error: {}'.format(e))