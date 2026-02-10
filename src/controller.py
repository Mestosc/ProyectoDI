import sqlite3

from libro import Libro


class Controller:
    def __init__(self, ):
        self.database_conn = sqlite3.connect('libros.db')
    
    def obtener_libro(self, bd_id: int) -> Libro:
        with self.database_conn as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM libros WHERE id = ?", (bd_id,))
            libro = cursor.fetchone()
            return Libro(id=libro[0][0], titulo=libro[0][1], paginas_leidas=libro[0][2], paginas_totales=libro[0][3])

    def insertar_libro(self,libro: Libro):
        with self.database_conn as db:
            cursor = db.cursor()
            v = cursor.execute("INSERT INTO libros VALUES (?,?,?,?)", (libro.id, libro.titulo,libro.paginas_leidas,libro.paginas_totales))
            db.commit()
            return v

    def actualizar_libro(self,libro: Libro):
        with self.database_conn as db:
            cursor = db.cursor()
            libro_comprobar = self.obtener_libro(libro.id)