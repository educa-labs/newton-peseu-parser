import psycopg2 as psql

dbg = "[DEBUG] "

class DB():

    def __init__(self):     
        self.conn = psql.connect("""
                dbname=datospsu 
                user=felipe 
                password=123abc456 
                host=localhost 
                port=5432""")
        self.cur = self.conn.cursor()
        self.cur_for = self.conn.cursor()

    def exec(self, query, *args):
        print(dbg,args)
        try:
            self.cur.execute(query, args)
            self.conn.commit()
        except Exception as e:
            # Exception don felipe
            print(dbg, "Error al hacer la consulta: ", query, "\n", "Error: ", e)
            raise Exception("Se cashooooo boludo")
        return

    def createTables(self):
        # Eliminar tablas
        self.cur.execute("DROP TABLE IF EXISTS students, scores, postulacion")
        self.conn.commit()
        # Crear tabla estudiantes
        self.exec("""
            CREATE TABLE students(id serial primary key, 
            rut text, name text, year int)""")
        # Crear tabla puntajes
        self.exec("""
            CREATE TABLE scores(id serial primary key,
            id_student int references students(id),
            mat int, len int, cie int, his int, nem int)""")
        # Crear tabla postulaciones
        self.exec("""
            CREATE TABLE postulacion(id_student int references students(id),
            carrera text, universidad text, year int)""")

    def insert_students_2013(self, filename):
        """ 
        insert_students_2013: metodo para ir subiendo a los usuarios. Lee el 
        nombre del archivo y va recorriendo el archivo.
        """
        # Agregar los estudiantes a la base de datos
        with open(filename+".csv", "r") as reader:
            reader.readline()
            for linea in reader:
                linea = linea.split(",")
                # Agregar los alumnos con rut, nombre, carrera y universidad
                self.exec("""
                    INSERT INTO students(rut, name, year) 
                    VALUES(%s,%s,%s,%s,%s)""", 
                    linea[0], linea[1], 2013)

    def insert_students_2014(self, filename):
        """
        Insert_students_2014: metodo para subir los usuarios del 2014. Lee el 
        nombre del archivo y lo recorre para ir subiendo los alumnos del año 2014.
        """
        with open(filename + '.csv', 'r') as reader:
            reader.readline()
            for linea in reader:
                linea = linea.split(',')
                # Agregar los alunos con rut, nombre, carrera y universidad
                self.exec("""
                    INSERT INTO students(rut, name, carrera, universidad, year)
                    VALUES(%s,%s,%s,%s,%s)""", 
                    None, linea[0], linea[3], linea[4].strip(), 2014)

    def insert_students_2015(self, filename):
        """
        Insert_students_2015: metodo para subir los usuarios del 2015. Lee el 
        nombre del archivo y lo recorre para ir subiendo los alumnos del 2015
        """
        with open(filename + '.csv', 'r') as reader:
            reader.readline()
            for linea in reader:
                linea = linea.split(',')
                self.exec("""
                    INSERT INTO students(rut, name, year)
                    VALUES(%s,%s,%s,%s,%s)""",
                    None, linea[0], 2015)

                # Agregar postulacion de alumno
                self.cur.execute("""
                    SELECT * FROM students WHERE name=%s;""",
                    (linea[0],))
                # Guardar el id del alumno recien subido
                ide_alumno = db.cur.fetchone()[0]
                # Guardar una postulacion del alumno
                self.cur.execute("""
                    INSERT INTO postulacion(id_student, carrera, universidad, year)
                    VALUES(%s,%s,%s,%s)""",
                    ide_alumno, linea[4].strip(), linea[3], 2015)

    def insertScore(self, ide, puntajes):
        """ 
        InsertScore: Metodo para subir los puntajes a la base de datos. Recibe 
        el id del usuario y los puntajes y lo sube.
        """
        id_student = ide
        leng = int(puntajes[0])
        mat = int(puntajes[1])
        cie = int(puntajes[2])
        his = int(puntajes[3])
        nem = int(puntajes[4])

        self.exec("""
            INSERT INTO scores(id_student, mat, len, cie, his, nem) 
            VALUES(%s,%s,%s,%s,%s,%s)""", 
            id_student, leng, mat, cie, his, nem)


if __name__ == "__main__":
    db = DB()
    db.createTables()
    # db.insert_students_2013("usuarios_peseu_2013")
    # db.insert_students_2014('usuarios_peseu_2014')
    db.insert_students_2015('usuarios_peseu_2015')
    db.conn.close()