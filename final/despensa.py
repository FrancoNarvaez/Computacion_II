ingredientes = {
    'Hamburguesa': 10,
    'Pizza': 5,
    'Ensalada': 8,
    'Refresco': 20,
    'Agua': 20,
    'Milanesa': 10,
    'Papas fritas': 15,
    'Hot dog': 10,
    'Tacos': 10
}


class Despensa:
    def __init__(self):
        self.ingredientes = ingredientes

    def agregar_ingrediente(self, ingrediente, cantidad):
        if ingrediente in self.ingredientes:
            self.ingredientes[ingrediente] += cantidad
        else:
            self.ingredientes[ingrediente] = cantidad

    def eliminar_ingrediente(self, ingrediente, cantidad):
        if ingrediente in self.ingredientes and self.ingredientes[ingrediente] >= cantidad:
            self.ingredientes[ingrediente] -= cantidad
        else:
            print("No hay suficientes ingredientes para eliminar")

    def verificar_cantidad(self, ingrediente):
        return self.ingredientes.get(ingrediente, 0)