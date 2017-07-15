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

def get_puntajes_2013(rut):
    data = [
        ('tipo', 'anteriores'),
        ('rut', rut),
        ('admision', '2013')
    ]

    pagina = requests.post(
        'http://www.peseu.com/busqueda', headers=headers, cookies=cookies, data=data)
    tree_puntajes = html.fromstring(pagina.content)
    puntajes_personas = tree_puntajes.xpath('//table/tr/td/text()')[2:]

    return puntajes_personas

if __name__ == "__main__":
    print(get_puntajes_2013("187206421"))