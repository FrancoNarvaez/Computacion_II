from celery import Celery
import time

app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

# Diccionario para rastrear la cantidad de cada ingrediente disponible por ahora, luego sera una DB
ingredientes = {
    'Hamburguesa': 10,
    'Pizza': 5,
    'Ensalada': 8
}

@app.task
def check_ingredients(order):
    # Verifica si hay suficientes ingredientes para cada producto en el pedido
    for producto_dict in order['productos']:
        producto = producto_dict['producto']
        cantidad = producto_dict['cantidad']

        # Si no hay suficientes ingredientes para un producto, devuelve 'Insuficiente'
        if ingredientes[producto] < cantidad:
            return 'Insuficiente'

    # Si hay suficientes ingredientes para todos los productos, devuelve 'Suficiente'
    return 'En proceso'

@app.task
def prepare_order(order):
    # Simula la preparación del pedido con un tiempo de espera
    time.sleep(10)
    return "Completado"