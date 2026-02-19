import gi

from controller import Controller
from formulario_anadir_datos import Formulario

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # noqa: E402


class Ventana(Gtk.Window):
    """

    Representacion de la ventana principal de la aplicacion

    """

    def __init__(self, controller: Controller):  # noqa: F811
        """

        Iniciar la ventana principal de la aplicacion
        :param controller: El controller de la aplicacion
        :type controller: Controller

        """
        super().__init__(title="Ventana principal")
        self.controller: Controller = controller
        self.modelo = Gtk.ListStore(int, str, str, int, int, str)
        self.anadir_valores_bd()
        layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        boton = Gtk.Button.new_with_mnemonic(label="_Añadir nuevo libro")
        _ = boton.connect("clicked", self.mostrar_formulario_anadir, self.controller)
        self.tabla = Gtk.TreeView(model=self.modelo)
        self.agregar_columna("ID", 0)
        self.agregar_columna("Titulo", 1)
        self.agregar_columna("Autor", 2)
        self.agregar_columna("Paginas Leidas", 3)
        self.agregar_columna("Paginas totales", 4)
        self.agregar_columna("Porcentaje leido", 5)
        layout.pack_start(self.tabla, True, True, 0)
        layout.pack_start(boton, False, True, 0)
        self.add(layout)
        self.show_all()

    def agregar_columna(self, titulo: str, indice: int):
        """

        Abstrae la agregacion de una columna a la tabla para no tener que ir creando el renderer y la columna de forma manual

        :param titulo: El titulo de la columna
        :type titulo: str
        :param indice: El indice de la columna
        :type indice: int

        """
        renderer = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn(titulo, renderer, text=indice)
        _ = self.tabla.append_column(columna)

    def mostrar_formulario_anadir(self, _button: Gtk.Button, controller: Controller):
        formulario_anadir = Formulario(controller, self)
        formulario_anadir.show_all()

    def anadir_valores_bd(self):
        """

        Añade valores de la base de datos en la tabla que usa la aplicacion visualmente
        :param modelo: El modelo de datos usado por GTK
        :type modelo: Gtk.ListStore

        """
        libros = self.controller.obtener_todos_libros()
        for libro in libros:
                self.modelo.append(
                    [
                        libro.id,
                        libro.titulo,
                        str(libro.autor),
                        libro.paginas_leidas,
                        libro.paginas_totales,
                        f"{libro.porcentaje_leido}%",
                    ]
                )


def iniciar_ventana(controller: Controller):
    """

    Incia la ventana principal, de la aplicacion
    :param controller: El controlador de la base de datos
    :type: Controller

    """
    Ventana(controller)
    Gtk.main()
