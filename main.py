import functions
import db as DB

if __name__  == "__main__":
    db = DB.DB()
    # Obtener el ultimo usuario que se subio
    db.cur.execute("SELECT max(id_student) FROM scores;")
    max_id = db.cur.fetchone()[0]
    # Si hay ultimo usuario se fija en ese
    if max_id:
    	db.cur_for.execute("SELECT id,rut FROM students WHERE id > %s;", (max_id,))
    # Si no hay ultimo usuario se executa desde cero
    else:
    	db.cur_for.execute("SELECT id,rut FROM students;")

    # Para cada alumno en la consulta
    for alumno in db.cur_for:
        ide = alumno[0]
        rut = alumno[1]
        print(DB.dbg, "ID alumno: {} - RUT: {}".format(ide,rut))
        print(DB.dbg, 'Carrera: {} - Universidad: {}'.format(alumno[2], alumno[3]))
        try:
            # Subir los puntajes
        	ptjes = functions.getInfo(rut)
        	db.insertScore(ide, ptjes)
        except Exception as e:
        	print(DB.dbg, "Error al procesar la informacion")
