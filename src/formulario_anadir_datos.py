import subprocess

import gi

from controller import Controller
from libro import Libro

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # noqa: E402


class Formulario(Gtk.Window):
    def __init__(self, controller: Controller,ventana_padre):
        super().__init__(title="Añadir nuevo libro")
        self.controller = controller
        self.ventana_padre = ventana_padre
        layout = Gtk.Grid()
        etiqueta_titulo = Gtk.Label(label="Titulo")
        self.titulo = Gtk.Entry(placeholder_text="Absurdeces del mundo")
        self.titulo.set_hexpand(
            True
        )  # Esto hace que el Entry use todo el espacio horizontal disponible
        layout.attach(etiqueta_titulo, 0, 0, 1, 1)  # Columna 0, Fila 0
        layout.attach_next_to(self.titulo, etiqueta_titulo, Gtk.PositionType.RIGHT, 1, 1)
        paginas_leidas_label = Gtk.Label(label="Paginas Leidas")
        self.paginas_leidas = Gtk.Entry(placeholder_text="0")
        layout.attach_next_to(
            paginas_leidas_label, etiqueta_titulo, Gtk.PositionType.BOTTOM, 1, 1
        )
        layout.attach_next_to(
            self.paginas_leidas, paginas_leidas_label, Gtk.PositionType.RIGHT, 1, 1
        )
        paginas_totales_label = Gtk.Label(label="Paginas Leidas")
        self.paginas_totales = Gtk.Entry(placeholder_text="0")
        layout.attach_next_to(
            paginas_totales_label, paginas_leidas_label, Gtk.PositionType.BOTTOM, 1, 1
        )
        layout.attach_next_to(
            self.paginas_totales, paginas_totales_label, Gtk.PositionType.RIGHT, 1, 1
        )
        autor_label = Gtk.Label(label="Autor")
        self.autor = Gtk.Entry(placeholder_text="Anonimo")
        layout.attach_next_to(
            autor_label, paginas_totales_label, Gtk.PositionType.BOTTOM, 1, 1
        )
        layout.attach_next_to(
            self.autor, autor_label, Gtk.PositionType.RIGHT, 1, 1
        )
        boton = Gtk.Button.new_with_mnemonic("_Añadir libro")
        boton.connect("clicked",self.anadir_libro)
        layout.attach(boton, 0, 4, 2, 1)
        self.add(layout)
    def anadir_libro(self, widget):
        try:
            p_leidas = int(self.paginas_leidas.get_text() or 0)
            p_totales = int(self.paginas_totales.get_text() or 0)
            autor = self.autor.get_text().strip() or "Desconocido"
            titulo = self.titulo.get_text().strip() or ""
            libro = Libro(titulo=titulo,paginas_leidas=p_leidas,paginas_totales=p_totales,autor=autor)
            self.controller.insertar_libro(libro)
            self.ventana_padre.modelo.clear()
            self.ventana_padre.anadir_valores_bd()
        except ValueError:
            subprocess.run(["notify-send", "No se puede introducir un libro cuyas paginas leidas sean mayores que las paginas totales o cuyas paginas no sean enteras"])

