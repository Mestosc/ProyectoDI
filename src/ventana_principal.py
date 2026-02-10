import gi

from controller import Controller

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Ventana(Gtk.Window):
    """

    Representacion de la ventana principal de la aplicacion

    """

    def __init__(self,controller: Controller):
        super().__init__(title="Ventana principal")
        modelo = Gtk.ListStore(int, str, int, int, float)
        layout = Gtk.BoxLayout(orientation=Gtk.Orientation.VERTICAL)
        self.tabla = Gtk.TreeView(model=modelo)
        self.agregar_columna("Titulo", 0)
        self.agregar_columna("Paginas Leidas", 1)
        self.agregar_columna("Paginas totales", 2)
        self.agregar_columna("Porcentaje leido", 3)
        layout.pack_start(
            self.tabla,
        )
        self.show()

    def agregar_columna(self, titulo: str, indice: int):
        """

        Abstrae la agregacion de una columna a la tabla para no tener que ir creando el renderer y la columna de forma manual

        """
        renderer = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn(titulo, renderer, text=indice)
        self.tabla.append_column(columna)


def iniciar_ventana(controller: Controller):
    Ventana(controller)
    Gtk.main()
