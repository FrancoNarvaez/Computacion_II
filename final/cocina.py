from celery import Celery, group
import time

app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

# Diccionario para rastrear la cantidad de cada ingrediente disponible por ahora, luego sera una DB si fuese necesario
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


@app.task
def check_ingredients(order):
    # Verifica si hay suficientes ingredientes para cada producto en el pedido
    for producto_dict in order['productos']:
        producto = producto_dict['producto']
        cantidad = producto_dict['cantidad']
        # Si no hay suficientes ingredientes para un producto, establece el estado a 'Insuficiente'
        if ingredientes[producto] < cantidad:
            order['estado'] = 'Insuficiente'
            print("Soy el order en check_ingredientes:\n", order, "\nNo hay sufiencientes ingredientes")
            return order

    # Si hay suficientes ingredientes para todos los productos, establece el estado a 'En proceso'
    order['estado'] = 'En proceso'
    return order


@app.task
def prepare_ensalada(order):
    # Simula la preparación del pedido con un tiempo de espera
    time.sleep(5)
    print("Ensalada preparada")
    for product in order['productos']:
        if product['producto'] == 'Ensalada':
            product['estado'] = 'Completado'
    return order


@app.task
def prepare_hamburgesa(order):
    # Simula la preparación del pedido con un tiempo de espera
    time.sleep(5)
    print("Hamburguesa preparada")
    for product in order['productos']:
        if product['producto'] == 'Hamburguesa':
            product['estado'] = 'Completado'
    return order


@app.task
def prepare_pizza(order):
    # Simula la preparación del pedido con un tiempo de espera
    time.sleep(5)
    print("Pizza preparada")
    for product in order['productos']:
        if product['producto'] == 'Pizza':
            product['estado'] = 'Completado'
    return order


@app.task
def prepare_refresco(order):
    # Simula la preparación del pedido con un tiempo de espera
    time.sleep(5)
    print("Refresco preparado")
    for product in order['productos']:
        if product['producto'] == 'Refresco':
            product['estado'] = 'Completado'
    return order


@app.task
def prepare_agua(order):
    # Simula la preparación del pedido con un tiempo de espera
    time.sleep(5)
    print("Agua preparada")
    for product in order['productos']:
        if product['producto'] == 'Agua':
            product['estado'] = 'Completado'
    return order


@app.task
def prepare_milanesa(order):
    # Simula la preparación del pedido con un tiempo de espera
    time.sleep(5)
    print("Milanesa preparada")
    for product in order['productos']:
        if product['producto'] == 'Milanesa':
            product['estado'] = 'Completado'
            print("Siguinte producto")
    return order


@app.task
def prepare_papas_fritas(order):
    # Simula la preparación del pedido con un tiempo de espera
    time.sleep(5)
    print("Papas fritas preparadas")
    for product in order['productos']:
        if product['producto'] == 'Papas fritas':
            product['estado'] = 'Completado'
            print("Siguinte producto")
    return order


@app.task
def prepare_hot_dog(order):
    # Simula la preparación del pedido con un tiempo de espera
    time.sleep(5)
    print("Hot dog preparado")
    for product in order['productos']:
        if product['producto'] == 'Hot dog':
            product['estado'] = 'Completado'
            print("Siguinte producto")
    return order


@app.task
def prepare_tacos(order):
    # Simula la preparación del pedido con un tiempo de espera
    time.sleep(5)
    print("Tacos preparados")
    for product in order['productos']:
        if product['producto'] == 'Tacos':
            product['estado'] = 'Completado'
            print("Siguinte producto")
    return order


@app.task
def prepare_order(order, callback=None):
    print("voy a prepara la orden")

    # Si hay suficientes ingredientes, inicia la preparación del pedido
    if order['estado'] == 'En proceso':
        # Crea una lista de tareas para cada producto en el pedido
        tasks = []
        for product in order['productos']:
            match product['producto']:
                case 'Hamburguesa':
                    tasks.append(prepare_hamburgesa.s(order))
                case 'Pizza':
                    tasks.append(prepare_pizza.s(order))
                case 'Ensalada':
                    tasks.append(prepare_ensalada.s(order))
                case 'Refresco':
                    tasks.append(prepare_refresco.s(order))
                case 'Agua':
                    tasks.append(prepare_agua.s(order))
                case 'Milanesa':
                    tasks.append(prepare_milanesa.s(order))
                case 'Papas fritas':
                    tasks.append(prepare_papas_fritas.s(order))
                case 'Hot dog':
                    tasks.append(prepare_hot_dog.s(order))
                case 'Tacos':
                    tasks.append(prepare_tacos.s(order))
                case _:
                    print("Producto no reconocido")

        print("Todas las ordenes pedidas\n")
        # Ejecuta todas las tareas en paralelo y luego ejecuta verify_order
        job = group(*tasks) | verify_order.s(order)
        return job
    else:
        print("No se puede preparar la orden debido a ingredientes insuficientes")
        return


@app.task
def verify_order(results, order):
    final_order = order.copy()
    # Crea un diccionario para rastrear los estados de los productos
    product_status = {}
    for result in results:
        for product in result['productos']:
            if 'estado' in product:
                product_status[product['producto']] = product['estado']

    # Actualiza el estado de los productos en final_order
    for product in final_order['productos']:
        if product['producto'] in product_status:
            product['estado'] = product_status[product['producto']]

    # Verifica si todos los productos están completados
    if all(product['estado'] == 'Completado' for product in final_order['productos']):
        final_order['estado'] = 'Completado'
        print("Orden completada\nFinal orden:", final_order)
    else:
        final_order['estado'] = 'Error'

    return final_order


@app.task(bind=True)
def handle_result(self, results):
    # Obtiene y muestra el resultado de la tarea
    print("Pedido completado:")
    final_order = results
    print(final_order)
    return final_order
