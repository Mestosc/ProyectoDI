import subprocess
from typing import TYPE_CHECKING

import gi

from controller import Controller
from libro import Libro

if TYPE_CHECKING:
    from ventana_principal import Ventana

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # noqa: E402

class FormularioAutores(Gtk.Window):
    ventana_padre: "Ventana"

    def __init__(self, controller: Controller, ventana_padre: "Ventana"):
        super().__init__(title="Añadir nuevo autor")
        self.controller: Controller = controller
        self.ventana_padre = ventana_padre
        
        layout = Gtk.Grid()
        layout.set_column_spacing(10)
        layout.set_row_spacing(10)
        layout.set_border_width(10)

        etiqueta_nombre = Gtk.Label(label="Nombre del Autor")
        self.nombre: Gtk.Entry = Gtk.Entry(placeholder_text="Nombre del autor")
        self.nombre.set_hexpand(True)
        
        layout.attach(etiqueta_nombre, 0, 0, 1, 1)
        layout.attach_next_to(self.nombre, etiqueta_nombre, Gtk.PositionType.RIGHT, 1, 1)
        
        boton = Gtk.Button.new_with_mnemonic("_Añadir autor")
        _ = boton.connect("clicked", self.anadir_autor)
        layout.attach(boton, 0, 1, 2, 1)
        
        super().add(layout)

    def anadir_autor(self, button: Gtk.Button):
        """
        Añade un nuevo autor a la base de datos.
        """
        nombre = self.nombre.get_text().strip()
        if not nombre:
            _ = subprocess.run(
                ["notify-send", "El nombre del autor no puede estar vacío"],
                check=False,
            )
            return

        exito = self.controller.insertar_autor(nombre)
        if exito:
            # Si el formulario de libros está abierto, tal vez querríamos refrescar sus sugerencias,
            # pero por ahora simplemente refrescamos la vista principal si fuera necesario.
            # Como la vista principal solo muestra libros, no hay cambio visual inmediato ahí
            # a menos que mostráramos una lista de autores.
            self.destroy()
        else:
            _ = subprocess.run(
                ["notify-send", f"Error: El autor '{nombre}' ya existe o hubo un error."],
                check=False,
            )

class Formulario(Gtk.Window):
    ventana_padre: "Ventana"

    def __init__(self, controller: Controller, ventana_padre: "Ventana"):
        super().__init__(title="Añadir nuevo libro")
        self.controller: Controller = controller
        self.ventana_padre = ventana_padre
        layout = Gtk.Grid()
        etiqueta_titulo = Gtk.Label(label="Titulo")
        self.titulo: Gtk.Entry = Gtk.Entry(placeholder_text="Absurdeces del mundo")
        self.titulo.set_hexpand(
            True
        )  # Esto hace que el Entry use todo el espacio horizontal disponible
        layout.attach(etiqueta_titulo, 0, 0, 1, 1)  # Columna 0, Fila 0
        layout.attach_next_to(
            self.titulo, etiqueta_titulo, Gtk.PositionType.RIGHT, 1, 1
        )
        paginas_leidas_label = Gtk.Label(label="Paginas Leidas")
        self.paginas_leidas: Gtk.Entry = Gtk.Entry(placeholder_text="0")
        layout.attach_next_to(
            paginas_leidas_label, etiqueta_titulo, Gtk.PositionType.BOTTOM, 1, 1
        )
        layout.attach_next_to(
            self.paginas_leidas, paginas_leidas_label, Gtk.PositionType.RIGHT, 1, 1
        )
        paginas_totales_label = Gtk.Label(label="Paginas Totales")
        self.paginas_totales: Gtk.Entry = Gtk.Entry(placeholder_text="0")
        layout.attach_next_to(
            paginas_totales_label, paginas_leidas_label, Gtk.PositionType.BOTTOM, 1, 1
        )
        layout.attach_next_to(
            self.paginas_totales, paginas_totales_label, Gtk.PositionType.RIGHT, 1, 1
        )
        autor_label: Gtk.Label = Gtk.Label(label="Autor")
        self.autor: Gtk.Entry = Gtk.Entry(placeholder_text="Nombre o ID del autor")
        
        # Completado de entrada para autores
        completado = Gtk.EntryCompletion()
        modelo_autores = Gtk.ListStore(str, str) # ID, Nombre
        autores = self.controller.obtener_todos_autores()
        for a in autores:
            modelo_autores.append([str(a.id), a.nombre])
        
        completado.set_model(modelo_autores)
        completado.set_text_column(1) # Muestra el nombre por defecto al sugerir
        # Permite buscar en ID o Nombre
        completado.set_match_func(lambda completion, key, iter: 
                                  key.lower() in modelo_autores[iter][0].lower() or 
                                  key.lower() in modelo_autores[iter][1].lower())
        
        self.autor.set_completion(completado)

        layout.attach_next_to(
            autor_label, paginas_totales_label, Gtk.PositionType.BOTTOM, 1, 1
        )
        layout.attach_next_to(self.autor, autor_label, Gtk.PositionType.RIGHT, 1, 1)
        boton = Gtk.Button.new_with_mnemonic("_Añadir libro")
        _ = boton.connect("clicked", self.anadir_libro)
        layout.attach(boton, 0, 4, 2, 1)
        super().add(layout)

    def anadir_libro(self, button: Gtk.Button):
        """

        Añadir un libro, a la base de datos y refrescar el modelo que representa la tabla en mi aplicacion, usando la informacion puesta en el forumulario si no se pone nada se emplean valores por defecto.

        """
        try:
            p_leidas = int(self.paginas_leidas.get_text() or 0)
            p_totales = int(self.paginas_totales.get_text() or 0)
            
            # Buscamos el autor por el texto de la entrada (nombre o ID)
            entrada_autor = self.autor.get_text().strip()
            if not entrada_autor:
                 _ = subprocess.run(
                    ["notify-send", "Debe introducir el nombre o ID de un autor"],
                    check=False,
                )
                 return

            autor = self.controller.buscar_autor(entrada_autor)
            
            if not autor:
                _ = subprocess.run(
                    [
                        "notify-send",
                        f"El autor '{entrada_autor}' no existe. Por favor, use uno existente.",
                    ],
                    check=False,
                )
                return

            titulo = self.titulo.get_text().strip() or ""
            libro = Libro(
                titulo=titulo,
                paginas_leidas=p_leidas,
                paginas_totales=p_totales,
                autor=autor,
            )
            _ = self.controller.insertar_libro(libro)
            self.ventana_padre.modelo.clear()
            self.ventana_padre.anadir_valores_bd()
            self.destroy()
        except ValueError:
            _ = subprocess.run(
                [
                    "notify-send",
                    "No se puede introducir un libro cuyas paginas leidas sean mayores que las paginas totales o cuyas paginas no sean enteras",
                ],
                check=False,
            )
