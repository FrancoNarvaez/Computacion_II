import time
from celery import group
from despensa import ingredientes
from prepare import prepare_hamburguesa, prepare_tacos, prepare_hot_dog, prepare_pizza, prepare_refresco, \
    prepare_ensalada, prepare_agua, prepare_milanesa, prepare_papas_fritas
from celery_app import app


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
    # Verifica si hay suficientes ingredientes para cada producto en el pedido
    for producto_dict in order_dict['productos']:
        producto = producto_dict['producto']
        cantidad = producto_dict['cantidad']
        # Si no hay suficientes ingredientes para un producto, establece el estado a 'Insuficiente'
        if ingredientes[producto] < cantidad:
            order_dict['estado'] = 'Insuficiente'
            print("Soy el order en check_ingredientes:\n", order_dict, "\nNo hay sufiencientes ingredientes")
            return order_dict

    # Si hay suficientes ingredientes para todos los productos, establece el estado a 'En proceso'
    order_dict['estado'] = 'Por preparar'
    print("Suficientes ingredientes para orden, a cocinar!!!!")
    return order_dict


@app.task
def prepare(order_dict):
    print("voy a prepara la orden")
    if order_dict['estado'] == 'Por preparar':
        print("Orden numero \n")
        print(order_dict['id_pedido'])
        print("en preparacion")
        # Crea una lista de tareas para cada producto en el pedido
        tasks = []
        for product in order_dict['productos']:
            prepare_function = product_to_function.get(product['producto'])
            if prepare_function:
                print(f"Toca preparar {product['producto']}")
                tasks.append(prepare_function.s(product))
            else:
                print("Producto no reconocido")

        print("Todas las ordenes pedidas\n")
        # Ejecuta todas las tareas en paralelo
        job = group(*tasks)
        results = job.apply_async()

        # Recoge los estados de los productos de las tareas
        for result in results.results:
            while result.state != 'SUCCESS':
                time.sleep(1)  # Espera un poco antes de revisar de nuevo
            product_name, product_status = result.result
            # Actualiza el estado del producto en la orden
            for product in order_dict['productos']:
                if product['producto'] == product_name:
                    product['estado'] = product_status
                    break

        # Verifica si todos los productos están completados
        if all(product.get('estado') == 'Completado' for product in order_dict['productos']):
            order_dict['estado'] = 'Completado'
        else:
            order_dict['estado'] = 'Error'

        return order_dict
