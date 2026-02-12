import gi

import controller
from controller import Controller
from formulario_anadir_datos import Formulario

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Ventana(Gtk.Window):
    """

    Representacion de la ventana principal de la aplicacion

    """

    def __init__(self, controller: Controller):
        super().__init__(title="Ventana principal")
        self.controller: Controller = controller
        modelo = Gtk.ListStore(int, str, int, int, str)
        self.anadir_valores_bd(modelo)
        layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        boton = Gtk.Button(label="Añadir nuevo libro")
        boton.connect("clicked", self.mostrar_formulario_anadir,self.controller)
        self.tabla = Gtk.TreeView(model=modelo)
        self.agregar_columna("ID",0)
        self.agregar_columna("Titulo", 1)
        self.agregar_columna("Paginas Leidas", 2)
        self.agregar_columna("Paginas totales", 3)
        self.agregar_columna("Porcentaje leido", 4)
        layout.pack_start(self.tabla, True, True, 0)
        layout.pack_start(boton, False, True, 0)
        self.add(layout)
        self.show_all()

    def agregar_columna(self, titulo: str, indice: int):
        """

        Abstrae la agregacion de una columna a la tabla para no tener que ir creando el renderer y la columna de forma manual

        """
        renderer = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn(titulo, renderer, text=indice)
        self.tabla.append_column(columna)

    def mostrar_formulario_anadir(self, evento, controller: Controller):
        self.formulario_anadir = Formulario(controller)
        self.formulario_anadir.show()

    def anadir_valores_bd(self, modelo: Gtk.ListStore):
        libros = self.controller.obtener_todos_libros()
        if libros:
            for libro in libros:
                modelo.append(
                    [
                        libro.id,
                        libro.titulo,
                        libro.paginas_leidas,
                        libro.paginas_totales,
                        f"{libro.porcentaje_leido}%",
                    ]
                )


def iniciar_ventana(controller: Controller):
    Ventana(controller)
    Gtk.main()
