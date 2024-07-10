import time

from celery import group
from app.despensa import ingredientes
from task.prepare import prepare_hamburguesa, prepare_tacos, prepare_hot_dog, prepare_pizza, prepare_refresco, \
    prepare_ensalada, prepare_agua, prepare_milanesa, prepare_papas_fritas
from app.celery_app import app

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
def check_ingredients(order_dict):
    for producto_dict in order_dict['productos']:
        producto = producto_dict['producto']
        cantidad = producto_dict['cantidad']
        if ingredientes[producto] < cantidad:
            order_dict['estado'] = 'Insuficiente'
            return order_dict
    order_dict['estado'] = 'Por preparar'
    return order_dict

@app.task
def prepare(order_dict):
    if order_dict['estado'] == 'Por preparar':
        tasks = []
        for product in order_dict['productos']:
            prepare_function = product_to_function.get(product['producto'])
            if prepare_function:
                tasks.append(prepare_function.s(product))
        job = group(*tasks)
        results = job.apply_async()
        for result in results.results:
            while result.state != 'SUCCESS':
                time.sleep(1)
            product_name, product_status = result.result
            for product in order_dict['productos']:
                if product['producto'] == product_name:
                    product['estado'] = product_status
                    break
        if all(product.get('estado') == 'Completado' for product in order_dict['productos']):
            order_dict['estado'] = 'Completado'
        else:
            order_dict['estado'] = 'Error'
        return order_dict
