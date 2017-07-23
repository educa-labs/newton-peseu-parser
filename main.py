import functions
from puntajes_peseu_2015 import (obtener_tupla_nombre, 
                                get_puntajes_2015)
import db as DB
import time
import threading

if __name__  == "__main__":
    db = DB.DB()
    # Obtener el ultimo usuario que se subio
    db.cur.execute("""
        SELECT max(id_student) FROM scores;""")
    max_id = db.cur.fetchone()[0]
    # Si hay ultimo usuario se fija en ese
    if max_id:
        db.cur_for.execute("""
            SELECT * FROM students WHERE id > 23743 AND id < 90692;
            """)
    ################################
    # CONSULTA ANTIGUA
    ################################
    #    db.cur_for.execute("""
    #        SELECT * FROM students WHERE id > %s;""", 
    #        (max_id,))
    # Si no hay ultimo usuario se executa desde cero
    else:
    	db.cur_for.execute("""
                SELECT * FROM students;""")
    # Para cada alumno en la consulta
    for alumno in db.cur_for:
        ide = alumno[0]
        rut = alumno[1]
        nombre_alumno = alumno[2]
        year = alumno[3]
        print(DB.dbg, "ID alumno: {} - RUT: {}".format(ide,rut))
        try:
            # Subir puntajes depende del año
            if year == 2013:
                # En el 2013 solo se suben con el rut
                time.sleep(2)
                inicio = time.time()
                ptjes = functions.getInfo(rut)
                final = time.time()
                print("[DEBUG] Se está demorando: {}".format((final - inicio)))
                db.insertScore(ide, ptjes)
            elif year == 2014:
                # En el 2014 no hay datos
                pass
            elif year == 2015:
                # En el 2015 se necesita el nombre
                time.sleep(2)
                inicio = time.time()
                nombre_tupla = obtener_tupla_nombre(nombre_alumno)
                ptjes = get_puntajes_2015(nombre_tupla)
                final = time.time()
                print("[DEBUG] Se está demorando: {}".format((final - inicio)))
                db.insertScore(ide, ptjes)
                

        except Exception as e:
            # En el caso que no tenga puntajes
        	print(DB.dbg, "Error al procesar la informacion: {}".format(e))