from sqlite3 import connect

from libro import Libro


class Controller:
    def __init__(self):
        self.database = 'libros.db'
    
    def obtener_libro(self, bd_id: int) -> Libro:
        with connect(self.database) as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM libros WHERE id = ?", (bd_id,))
            libro = cursor.fetchone()
            return Libro(id=libro[0][0], titulo=libro[0][1], paginas_leidas=libro[0][2], paginas_totales=libro[0][3])

    def insertar_libro(self,libro: Libro):
        with connect(self.database) as db:
            cursor = db.cursor()
            v = cursor.execute("INSERT INTO libros VALUES (?,?,?)", (libro.titulo,libro.paginas_leidas,libro.paginas_totales))
            db.commit()
            return v

    def actualizar_libro(self,libro: Libro):
        with connect(self.database) as db:
            cursor = db.cursor()
            libro_comprobar = self.obtener_libro(libro.id)