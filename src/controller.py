class Controller:
    def __init__(self, model, database):
        self.model = model
        self.database = database
    
    def obtener_libro() -> Libro:
        
