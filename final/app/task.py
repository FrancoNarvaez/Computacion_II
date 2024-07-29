import time

from celery import group
from app.despensa import ingredientes
from task.prepare import prepare_hamburguesa, prepare_tacos, prepare_hot_dog, prepare_pizza, prepare_refresco, \
    prepare_ensalada, prepare_agua, prepare_milanesa, prepare_papas_fritas
from app.celery_app import app

# Diccionario que mapea cada producto a su función de preparación correspondiente
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

    # Itera sobre cada producto en el pedido
    for producto_dict in order_dict['productos']:
        producto = producto_dict['producto']
        cantidad = producto_dict['cantidad']

        # Verifica si hay suficientes ingredientes para el producto
        if ingredientes[producto] < cantidad:
            # Si no hay suficientes ingredientes, actualiza el estado del producto y del pedido
            producto_dict['estado'] = 'Insuficiente'
            order_dict['estado'] = 'Insuficiente'
            return order_dict
        # Si hay suficientes ingredientes para todos los productos, actualiza el estado del pedido
    order_dict['estado'] = 'Por preparar'
    return order_dict


@app.task
def prepare(order_dict):
    # Verifica si el pedido está listo para ser preparado
    if order_dict['estado'] == 'Por preparar':
        tasks = []
        # Itera sobre cada producto en el pedido
        for product in order_dict['productos']:
            # Obtiene la función de preparación correspondiente al producto
            prepare_function = product_to_function.get(product['producto'])
            if prepare_function:
                # Agrega la tarea a la lista de tareas
                tasks.append(prepare_function.s(product))
            else:
                # Si no existe una función de preparación para el producto, actualiza el estado del producto
                product['estado'] = 'Error'
        if tasks:
            # Crea un grupo de tareas de Celery y las ejecuta
            job = group(*tasks)
            results = job.apply_async()
            # Espera a que todas las tareas se completen
            for result in results.results:
                while result.state != 'SUCCESS':
                    time.sleep(1)
                product_name, product_status = result.result
                # Actualiza el estado de cada producto basado en el resultado de la tarea
                for product in order_dict['productos']:
                    if product['producto'] == product_name:
                        product['estado'] = product_status
                        break

        # Verifica si todos los productos fueron preparados correctamente
        if all(product.get('estado') == 'Completado' for product in order_dict['productos']):
            order_dict['estado'] = 'Completado'
        else:
            order_dict['estado'] = 'Error'
    return order_dict
