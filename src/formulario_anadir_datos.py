import gi

from controller import Controller

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # noqa: E402


class Formulario(Gtk.Window):
    def __init__(self,controller: Controller):
        super().__init__(title="Añadir nuevo libro")
        self.controller = controller

