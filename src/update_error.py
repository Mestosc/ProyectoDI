class UpdateError(Exception):
    def __init__(self, error="Error actualizando los datos de la BD"):
        super().__init__(error)
