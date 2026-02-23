import unittest
import os
from controller import Controller
from libro import Libro, Autor
from update_error import UpdateError

class TestControllerExhaustivo(unittest.TestCase):
    def setUp(self):
        self.db_path = "test_stress_libros.db"
        # Aseguramos un estado limpio
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.controller = Controller(self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_persistencia_entre_instancias(self):
        """

        Verifica que los datos persisten si cerramos y abrimos el controlador.

        """
        autor = Autor(nombre="Autor Persistente")
        libro = Libro(titulo="Persistente", paginas_totales=100, autor=autor)
        self.controller.insertar_libro(libro)
        
        # Nueva instancia del controlador
        otro_controller = Controller(self.db_path)
        libros = otro_controller.obtener_todos_libros()
        self.assertEqual(len(libros), 1)
        self.assertEqual(libros[0].titulo, "Persistente")
        self.assertIsInstance(libros[0].autor, Autor)
        self.assertEqual(libros[0].autor.nombre, "Autor Persistente")

    def test_autor_como_string(self):
        """

        Verifica que insertar un libro con autor como string funciona (retrocompatibilidad).

        """
        libro = Libro(titulo="Libro String", autor="Autor String", paginas_totales=100)
        self.assertTrue(self.controller.insertar_libro(libro))
        
        recuperado = self.controller.obtener_libro(1)
        self.assertIsInstance(recuperado.autor, Autor)
        self.assertEqual(recuperado.autor.nombre, "Autor String")

    def test_mismo_autor_varios_libros(self):
        """

        Verifica que varios libros pueden compartir el mismo registro de autor.

        """
        nombre_autor = "Autor Compartido"
        l1 = Libro(titulo="Libro 1", autor=nombre_autor, paginas_totales=100)
        l2 = Libro(titulo="Libro 2", autor=nombre_autor, paginas_totales=200)
        
        self.controller.insertar_libro(l1)
        self.controller.insertar_libro(l2)
        
        # Verificar en la BD que solo hay un autor
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM autores")
        count = cursor.fetchone()[0]
        conn.close()
        
        self.assertEqual(count, 1)
        
        libros = self.controller.obtener_todos_libros()
        self.assertEqual(libros[0].autor.id, libros[1].autor.id)

    def test_actualizar_autor_libro(self):
        """Verifica que se puede cambiar el autor de un libro."""
        libro = Libro(titulo="Titulo Original", autor="Autor Original", paginas_totales=100)
        self.controller.insertar_libro(libro)
        
        recuperado = self.controller.obtener_libro(1)
        recuperado.autor = "Autor Nuevo"
        self.controller.actualizar_libro(recuperado)
        
        final = self.controller.obtener_libro(1)
        self.assertEqual(final.autor.nombre, "Autor Nuevo")

    def test_intento_inyeccion_sql(self):
        """Intenta romper el sistema con strings maliciosos."""
        malicious_title = "'; DROP TABLE libros; --"
        libro = Libro(titulo=malicious_title, paginas_totales=100)
        self.controller.insertar_libro(libro)
        
        # Si la inyección funcionara, la tabla no existiría o el libro no se recuperaría bien
        recuperado = self.controller.obtener_libro(1)
        self.assertIsNotNone(recuperado)
        self.assertEqual(recuperado.titulo, malicious_title)
        
        # Verificar que la tabla sigue ahí
        self.assertTrue(len(self.controller.obtener_todos_libros()) > 0)

    def test_datos_extremos(self):
        """Prueba con valores muy grandes o strings masivos."""
        long_title = "A" * 10000
        libro = Libro(titulo=long_title, paginas_totales=999999, paginas_leidas=500)
        self.assertTrue(self.controller.insertar_libro(libro))
        
        recuperado = self.controller.obtener_libro(1)
        self.assertEqual(recuperado.titulo, long_title)

    def test_actualizacion_sin_cambios(self):
        """Verifica que actualizar con los mismos datos no rompe nada."""
        libro = Libro(titulo="Igual", paginas_totales=100)
        self.controller.insertar_libro(libro)
        
        original = self.controller.obtener_libro(1)
        exito = self.controller.actualizar_libro(original)
        self.assertTrue(exito)
        
        final = self.controller.obtener_libro(1)
        self.assertEqual(original.titulo, final.titulo)

    def test_violacion_logica_negocio(self):
        """
        Verifica que el controlador/modelo maneja errores de lógica.
        (Ej: más páginas leídas que totales)
        """
        libro = Libro(titulo="Libro Base", paginas_totales=100, paginas_leidas=0)
        self.controller.insertar_libro(libro)
        
        # Intentamos crear un objeto libro inválido para actualizar
        # El modelo Libro ya debería lanzar ValueError según su código
        with self.assertRaises(ValueError):
            Libro(id=1, titulo="Invalido", paginas_totales=10, paginas_leidas=50)

    def test_caracteres_especiales_y_unicode(self):
        """Prueba con emojis y caracteres de otros idiomas."""
        unicode_title = "Libro de Python 🐍 漢 🌍"
        libro = Libro(titulo=unicode_title, paginas_totales=100)
        self.controller.insertar_libro(libro)
        
        recuperado = self.controller.obtener_libro(1)
        self.assertEqual(recuperado.titulo, unicode_title)

    def test_ids_negativos_o_invalidos(self):
        """Verifica comportamiento ante IDs absurdos."""
        self.assertIsNone(self.controller.obtener_libro(-1))
        self.assertIsNone(self.controller.obtener_libro(0))
        self.assertIsNone(self.controller.obtener_libro(999999))

    def test_actualizar_libro_sin_id(self):
        """Verifica que no se puede actualizar un libro que no tiene ID asignado."""
        libro = Libro(titulo="Sin ID", paginas_totales=100)
        self.assertFalse(self.controller.actualizar_libro(libro))

if __name__ == "__main__":
    unittest.main()
