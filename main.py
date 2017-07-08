import functions
import db as DB

if __name__  == "__main__":
    db = DB.DB()
    db.cur.execute("SELECT max(id_student) FROM scores;")
    max_id = db.cur.fetchone()[0]
    if max_id:
    	db.cur_for.execute("SELECT id,rut FROM students WHERE id > %s;", (max_id,))
    else:
    	db.cur_for.execute("SELECT id,rut FROM students;")

    for alumno in db.cur_for:
        ide = alumno[0]
        rut = alumno[1]
        print(DB.dbg, "ID alumno: {} - RUT: {}".format(ide,rut))
        try:
        	ptjes = functions.getInfo("187206421")
        	db.insertScore(ide, ptjes)
        except Exception as e:
        	print(DB.dbg, "Error al procesar la informacion")
        	exit(0)