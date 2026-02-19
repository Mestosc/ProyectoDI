import sqlite3
from dataclasses import asdict
from sqlite3 import Connection

from libro import Libro, Autor
from update_error import UpdateError


class Controller:
    def __init__(self, database: str = "../libros.db"):
        """
        Inicializa el controlador. El uso de la base de datos se gestiona
        mediante gestores de contexto para asegurar la integridad.

        :param database: Nombre del archivo de la base de datos.
        :type database: str

        """
        self.database: str = database
        self._inicializar_db()

    def _conexion(self) -> Connection:
        """

        Retorna la conexión (que es un gestor de contextos para transacciones).

        """
        return sqlite3.connect(self.database)

    def _inicializar_db(self):
        """

        Inicializa el esquema si es necesario, manejando la migración a autores.

        """
        try:
            with self._conexion() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                # Create autores table
                _ = cursor.execute("""
                    CREATE TABLE IF NOT EXISTS autores (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL UNIQUE
                    )
                """)

                # Check if libros table exists and its structure
                _ = cursor.execute(
                    "SELECT sql FROM sqlite_master WHERE type='table' AND name='libros'"
                )
                row = cursor.fetchone()
                if not row:
                    _ = cursor.execute("""
                        CREATE TABLE libros (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            titulo TEXT NOT NULL,
                            autor_id INTEGER NOT NULL,
                            paginas_leidas INTEGER DEFAULT 0,
                            paginas_totales INTEGER DEFAULT 0,
                            FOREIGN KEY (autor_id) REFERENCES autores(id)
                        )
                    """)
                elif "autor_id" not in row["sql"].lower():
                    # Migration: Change autor (TEXT) to autor_id (INTEGER)
                    print("Migrando base de datos a nuevo esquema...")
                    # 1. Get unique authors and insert into autores
                    _ = cursor.execute("SELECT DISTINCT autor FROM libros")
                    autores_antiguos = [r[0] for r in cursor.fetchall()]
                    for autor in autores_antiguos:
                        if autor is None:
                            autor = "Desconocido"
                        _ = cursor.execute(
                            "INSERT OR IGNORE INTO autores (nombre) VALUES (?)",
                            (autor,),
                        )

                    # 2. Create temporary table with new schema
                    _ = cursor.execute("""
                        CREATE TABLE libros_nuevo (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            titulo TEXT NOT NULL,
                            autor_id INTEGER NOT NULL,
                            paginas_leidas INTEGER DEFAULT 0,
                            paginas_totales INTEGER DEFAULT 0,
                            FOREIGN KEY (autor_id) REFERENCES autores(id)
                        )
                    """)

                    # 3. Copy data mapping authors to IDs
                    _ = cursor.execute("""
                        INSERT INTO libros_nuevo (id, titulo, autor_id, paginas_leidas, paginas_totales)
                        SELECT l.id, l.titulo, a.id, l.paginas_leidas, l.paginas_totales
                        FROM libros l
                        JOIN autores a ON COALESCE(l.autor, 'Desconocido') = a.nombre
                    """)

                    # 4. Swap tables
                    _ = cursor.execute("DROP TABLE libros")
                    _ = cursor.execute("ALTER TABLE libros_nuevo RENAME TO libros")
                    print("Migración completada.")
        except sqlite3.Error as e:
            print(f"Error crítico al inicializar la base de datos: {e}")

    def _obtener_o_crear_autor(self, cursor, autor_info) -> int:
        """

        Helper para obtener el ID de un autor a partir de un string o un objeto Autor.
        :param cursor: cursor de la base de datos a obtener.
        :type cursor: sqlite3.Cursor
        :param autor_info: objeto de la base de datos a obtener.
        :type autor_info: Autor

        """
        if autor_info is None:
            nombre = "Desconocido"
        elif isinstance(autor_info, Autor):
            nombre = autor_info.nombre
        else:
            nombre = str(autor_info)

        _ = cursor.execute("SELECT id FROM autores WHERE nombre = ?", (nombre,))
        row = cursor.fetchone()
        if row:
            return row[0]

        _ = cursor.execute("INSERT INTO autores (nombre) VALUES (?)", (nombre,))
        return cursor.lastrowid

    def obtener_libro(self, bd_id: int) -> Libro | None:
        """
        Recupera un libro por su ID utilizando el gestor de contextos.
        """
        try:
            with self._conexion() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                _ = cursor.execute("""
                    SELECT l.id, l.titulo, a.id as autor_id, a.nombre as autor_nombre,
                           l.paginas_leidas, l.paginas_totales
                    FROM libros l
                    JOIN autores a ON l.autor_id = a.id
                    WHERE l.id = ?
                """, (bd_id,))
                f = cursor.fetchone()
                if f:
                    autor = Autor(id=f["autor_id"], nombre=f["autor_nombre"])
                    return Libro(
                        id=f["id"],
                        autor=autor,
                        titulo=f["titulo"],
                        paginas_leidas=f["paginas_leidas"],
                        paginas_totales=f["paginas_totales"],
                    )
        except sqlite3.Error as e:
            print(f"Error al obtener el libro {bd_id}: {e}")
        return None

    def obtener_todos_libros(self) -> list[Libro]:
        """
        Retorna todos los libros registrados o una lista vacía.
        """
        try:
            with self._conexion() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                _ = cursor.execute("""
                    SELECT l.id, l.titulo, a.id as autor_id, a.nombre as autor_nombre,
                           l.paginas_leidas, l.paginas_totales
                    FROM libros l
                    JOIN autores a ON l.autor_id = a.id
                    ORDER BY l.id
                """)
                filas = cursor.fetchall()
                resultado = []
                for f in filas:
                    autor = Autor(id=f["autor_id"], nombre=f["autor_nombre"])
                    resultado.append(Libro(
                        id=f["id"],
                        titulo=f["titulo"],
                        autor=autor,
                        paginas_leidas=f["paginas_leidas"],
                        paginas_totales=f["paginas_totales"]
                    ))
                return resultado
        except sqlite3.Error as e:
            print(f"Error al obtener los libros: {e}")
            return []

    def insertar_libro(self, libro: Libro) -> bool:
        """

        Inserta un libro y retorna True si la operación fue exitosa.

        """
        try:
            with self._conexion() as conn:
                cursor = conn.cursor()
                autor_id = self._obtener_o_crear_autor(cursor, libro.autor)
                _ = cursor.execute(
                    "INSERT INTO libros (titulo, autor_id, paginas_leidas, paginas_totales) VALUES (?,?,?,?)",
                    (
                        libro.titulo,
                        autor_id,
                        libro.paginas_leidas,
                        libro.paginas_totales,
                    ),
                )
                return True
        except sqlite3.Error as e:
            print(f"Error al insertar el libro: {e}")
            return False

    def actualizar_libro(self, libro: Libro) -> bool:
        """

        Actualiza los campos modificados de un libro.

        """
        if libro.id is None:
            return False

        libro_ant = self.obtener_libro(libro.id)
        if not libro_ant:
            raise UpdateError(f"No existe el libro con ID {libro.id}")

        try:
            with self._conexion() as conn:
                cursor = conn.cursor()

                # Handle author update separately
                autor_id = self._obtener_o_crear_autor(cursor, libro.autor)

                _ = cursor.execute("""
                    UPDATE libros
                    SET titulo = ?, autor_id = ?, paginas_leidas = ?, paginas_totales = ?
                    WHERE id = ?
                """, (
                    libro.titulo,
                    autor_id,
                    libro.paginas_leidas,
                    libro.paginas_totales,
                    libro.id
                ))
                return True
        except sqlite3.Error as e:
            print(f"Error al actualizar el libro {libro.id}: {e}")
            return False

