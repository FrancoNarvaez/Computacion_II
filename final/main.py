from order import Order
from prepare import prepare_hamburguesa, prepare_pizza, prepare_ensalada, prepare_refresco, prepare_agua, prepare_milanesa, prepare_papas_fritas, prepare_hot_dog, prepare_tacos
from configRedis import app

# Mapea los nombres de los productos a las funciones de preparación
product_to_function = {
    'Hamburguesa': prepare_hamburguesa,
    'Pizza': prepare_pizza,
    'Ensalada': prepare_ensalada,
    'Refresco': prepare_refresco,
    'Agua': prepare_agua,
    'Milanesa': prepare_milanesa,
    'Papas fritas': prepare_papas_fritas,
    'Hot dog': prepare_hot_dog,
    'Tacos': prepare_tacos,
}


@app.task
def prepare_order(order_dict):
    order = Order(order_dict)
    return order.prepare(product_to_function)