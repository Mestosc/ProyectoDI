import gi

from controller import Controller
from formulario_anadir_datos import Formulario, FormularioAutores

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
        
        # Botones de accion
        box_botones = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        
        boton_libro = Gtk.Button.new_with_mnemonic(label="_Añadir nuevo libro")
        _ = boton_libro.connect("clicked", self.mostrar_formulario_anadir, self.controller)
        
        boton_autor = Gtk.Button.new_with_mnemonic(label="Añadir nuevo _autor")
        _ = boton_autor.connect("clicked", self.mostrar_formulario_autor, self.controller)

        boton_editar = Gtk.Button.new_with_mnemonic(label="_Editar seleccionado")
        _ = boton_editar.connect("clicked", self.on_editar_clicked)

        boton_eliminar = Gtk.Button.new_with_mnemonic(label="E_liminar seleccionado")
        _ = boton_eliminar.connect("clicked", self.on_eliminar_clicked)
        
        box_botones.pack_start(boton_libro, True, True, 0)
        box_botones.pack_start(boton_autor, True, True, 0)
        box_botones.pack_start(boton_editar, True, True, 0)
        box_botones.pack_start(boton_eliminar, True, True, 0)

        self.tabla = Gtk.TreeView(model=self.modelo)
        _ = self.tabla.connect("row-activated", self.on_row_activated)
        self.agregar_columna("ID", 0)
        self.agregar_columna("Titulo", 1)
        self.agregar_columna("Autor", 2)
        self.agregar_columna("Paginas Leidas", 3)
        self.agregar_columna("Paginas totales", 4)
        self.agregar_columna("Porcentaje leido", 5)
        
        layout.pack_start(self.tabla, True, True, 0)
        layout.pack_start(box_botones, False, True, 0)
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

    def mostrar_formulario_autor(self, _button: Gtk.Button, controller: Controller):
        formulario_autor = FormularioAutores(controller, self)
        formulario_autor.show_all()

    def get_libro_seleccionado(self):
        seleccion = self.tabla.get_selection()
        modelo, iterador = seleccion.get_selected()
        if iterador:
            libro_id = modelo.get_value(iterador, 0)
            return self.controller.obtener_libro(libro_id)
        return None

    def on_editar_clicked(self, _button):
        libro = self.get_libro_seleccionado()
        if libro:
            formulario = Formulario(self.controller, self, libro)
            formulario.show_all()

    def on_eliminar_clicked(self, _button):
        libro = self.get_libro_seleccionado()
        if libro:
            # Diálogo de confirmación simple
            dialogo = Gtk.MessageDialog(
                transient_for=self,
                flags=0,
                message_type=Gtk.MessageType.QUESTION,
                buttons=Gtk.ButtonsType.YES_NO,
                text=f"¿Estás seguro de que quieres eliminar '{libro.titulo}'?",
            )
            respuesta = dialogo.run()
            if respuesta == Gtk.ResponseType.YES:
                self.controller.eliminar_libro(libro.id)
                self.modelo.clear()
                self.anadir_valores_bd()
            dialogo.destroy()

    def on_row_activated(self, _treeview, _path, _column):
        self.on_editar_clicked(None)

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
