import sqlite3
from dataclasses import asdict
from sqlite3 import Connection

from libro import Libro
from update_error import UpdateError


class Controller:
    def __init__(self, database: str = "../libros.db"):
        """
        Inicializa el controlador. El uso de la base de datos se gestiona
        mediante gestores de contexto para asegurar la integridad.
        """
        self.database: str = database
        self._inicializar_db()

    def _conexion(self) -> Connection:
        """
        Retorna la conexión (que es un gestor de contextos para transacciones).
        """
        return sqlite3.connect(self.database)

    def _inicializar_db(self):
        """Inicializa el esquema si es necesario."""
        try:
            with self._conexion() as conn:
                cursor = conn.cursor()
                _ = cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='libros'"
                )
                if not cursor.fetchone():
                    _ = cursor.execute("""
                        CREATE TABLE libros (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            titulo TEXT NOT NULL,
                            autor TEXT NOT NULL,
                            paginas_leidas INTEGER DEFAULT 0,
                            paginas_totales INTEGER DEFAULT 0
                        )
                    """)
        except sqlite3.Error as e:
            print(f"Error crítico al inicializar la base de datos: {e}")

    def obtener_libro(self, bd_id: int) -> Libro | None:
        """
        Recupera un libro por su ID utilizando el gestor de contextos.

        :param bd_id: El id del libro en la base de datos
        :type bd_id: int
        :return El libro o Nada
        :rtype: Libro | None


        """
        try:
            with self._conexion() as conn:
                conn.row_factory = sqlite3.Row  # Nos permite usar los nombres de las columnas de una tabla para referirnos a cada dato
                cursor = conn.cursor()
                _ = cursor.execute(
                    "SELECT id, titulo, autor, paginas_leidas, paginas_totales FROM libros WHERE id = ?",
                    (bd_id,),
                )
                f = cursor.fetchone()
                if f:
                    return Libro(
                        id=f["id"],
                        autor=f["autor"],
                        titulo=f["titulo"],
                        paginas_leidas=f["paginas_leidas"],
                        paginas_totales=f["paginas_totales"],
                    )
        except sqlite3.Error as e:
            print(f"Error al obtener el libro {bd_id}: {e}")
        return None

    def obtener_todos_libros(self) -> list[Libro]:
        """Retorna todos los libros registrados o una lista vacía."""
        try:
            with self._conexion() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                _ = cursor.execute(
                    "SELECT id, titulo, autor, paginas_leidas, paginas_totales FROM libros ORDER BY id"
                )
                filas = cursor.fetchall()
                return [Libro(**dict(f)) for f in filas]
        except sqlite3.Error as e:
            print(f"Error al obtener los libros: {e}")
            return []

    def insertar_libro(self, libro: Libro) -> bool:
        """Inserta un libro y retorna True si la operación fue exitosa."""
        try:
            with self._conexion() as conn:
                cursor = conn.cursor()
                _ = cursor.execute(
                    "INSERT INTO libros (titulo, autor, paginas_leidas, paginas_totales) VALUES (?,?,?,?)",
                    (libro.titulo, libro.autor, libro.paginas_leidas, libro.paginas_totales),
                )
                return True
        except sqlite3.Error as e:
            print(f"Error al insertar el libro: {e}")
            return False

    def actualizar_libro(self, libro: Libro) -> bool:
        """
        Actualiza los campos modificados de un libro.
        Lanza UpdateError si el libro no existe.
        """
        if libro.id is None:
            return False

        libro_ant = self.obtener_libro(libro.id)
        if not libro_ant:
            raise UpdateError(f"No existe el libro con ID {libro.id}")

        l_act_dict = asdict(libro)
        l_ant_dict = asdict(libro_ant)

        columnas = {"titulo", "paginas_leidas", "paginas_totales", "autor"}
        cambios = {
            k: v
            for k, v in l_act_dict.items()
            if k in columnas and v != l_ant_dict.get(k)
        }

        if not cambios:
            return True

        try:
            with self._conexion() as conn:
                sql = f"UPDATE libros SET {', '.join(f'{k} = ?' for k in cambios)} WHERE id = ?"
                _ = conn.execute(sql, (*cambios.values(), libro.id))
                return True
        except sqlite3.Error as e:
            print(f"Error al actualizar el libro {libro.id}: {e}")
            return False
