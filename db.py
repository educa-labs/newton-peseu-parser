import psycopg2 as psql

dbg = "[DEBUG] "
class DB():

    def __init__(self):     
        self.conn = psql.connect("dbname=datospsu user=felipe password=123abc456 host=localhost port=5432")
        self.cur = self.conn.cursor()
        self.cur_for = self.conn.cursor()

    def exec(self, query, *args):
        print(dbg,args)
        try:
            self.cur.execute(query, args)
            self.conn.commit()
        except Exception as e:
            print(dbg, "Error al hacer la consulta: ", query, "\n", "Error: ", e)
            raise Exception("Se cashooooo boludo")
        return

    def createTables(self):
        self.cur.execute("DROP TABLE IF EXISTS students, scores")
        self.conn.commit()
        self.exec("""CREATE TABLE students(id serial primary key, rut text, name text)""")
        self.exec("""CREATE TABLE scores(id serial primary key,
                                         id_student int references students(id),
                                         mat int, len int, cie int,
                                          his int, nem int)""")

    def insertStudents(self, filename):
        with open(filename+".csv", "r") as reader:
            reader.readline()
            for linea in reader:
                linea = linea.split(",")
                # print(linea)
                self.exec("INSERT INTO students(rut, name) VALUES(%s,%s)", linea[0], linea[1])


    def insertScore(self, ide, puntajes):
        id_student = ide
        leng = int(puntajes[0])
        mat = int(puntajes[1])
        cie = int(puntajes[2])
        his = int(puntajes[3])
        nem = int(puntajes[4])

        self.exec("INSERT INTO scores(id_student, mat, len, cie, his, nem) VALUES(%s,%s,%s,%s,%s,%s)", id_student, leng, mat, cie, his, nem)



if __name__ == "__main__":
    db = DB()
    db.createTables()
    db.insertStudents("usuarios")
    db.conn.close()

