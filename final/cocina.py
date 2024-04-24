from celery import Celery, group
import time

app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
app.conf.broker_connection_retry_on_startup = True

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
    order['estado'] = 'Por preparar'
    return order


@app.task
def prepare_ensalada(order):
    # Simula la preparación del pedido con un tiempo de espera
    time.sleep(5)
    for product in order['productos']:
        if product['producto'] == 'Ensalada':
            print("Ensalada preparada")
            product['estado'] = 'Completado'
    return all(product.get('estado') == 'Completado' for product in order['productos'])


@app.task
def prepare_hamburgesa(order):
    # Simula la preparación del pedido con un tiempo de espera
    time.sleep(5)
    for product in order['productos']:
        if product['producto'] == 'Hamburguesa':
            print("Hamburguesa preparada")
            product['estado'] = 'Completado'
        return all(product.get('estado') == 'Completado' for product in order['productos'])


@app.task
def prepare_pizza(order):
    # Simula la preparación del pedido con un tiempo de espera
    time.sleep(5)
    for product in order['productos']:
        if product['producto'] == 'Pizza':
            print("Pizza preparada")
            product['estado'] = 'Completado'
        return all(product.get('estado') == 'Completado' for product in order['productos'])


@app.task
def prepare_refresco(order):
    # Simula la preparación del pedido con un tiempo de espera
    time.sleep(5)
    for product in order['productos']:
        if product['producto'] == 'Refresco':
            print("Refresco preparado")
            product['estado'] = 'Completado'
        return all(product.get('estado') == 'Completado' for product in order['productos'])


@app.task
def prepare_agua(order):
    # Simula la preparación del pedido con un tiempo de espera
    time.sleep(5)
    for product in order['productos']:
        if product['producto'] == 'Agua':
            print("Agua preparada")
            product['estado'] = 'Completado'
        return all(product.get('estado') == 'Completado' for product in order['productos'])


@app.task
def prepare_milanesa(order):
    # Simula la preparación del pedido con un tiempo de espera
    time.sleep(5)
    for product in order['productos']:
        if product['producto'] == 'Milanesa':
            print("Milanesa preparada")
            product['estado'] = 'Completado'
        return all(product.get('estado') == 'Completado' for product in order['productos'])


@app.task
def prepare_papas_fritas(order):
    # Simula la preparación del pedido con un tiempo de espera
    time.sleep(5)
    for product in order['productos']:
        if product['producto'] == 'Papas fritas':
            print("Papas fritas preparadas")
            product['estado'] = 'Completado'
        return all(product.get('estado') == 'Completado' for product in order['productos'])


@app.task
def prepare_hot_dog(order):
    # Simula la preparación del pedido con un tiempo de espera
    time.sleep(5)
    for product in order['productos']:
        if product['producto'] == 'Hot dog':
            print("Hot dog preparado")
            product['estado'] = 'Completado'
        return all(product.get('estado') == 'Completado' for product in order['productos'])


@app.task
def prepare_tacos(order):
    # Simula la preparación del pedido con un tiempo de espera
    time.sleep(5)
    for product in order['productos']:
        if product['producto'] == 'Tacos':
            print("Tacos preparados")
            product['estado'] = 'Completado'
        return all(product.get('estado') == 'Completado' for product in order['productos'])


@app.task
def prepare_order(order):
    print("voy a prepara la orden")

    # Si hay suficientes ingredientes, inicia la preparación del pedido
    if order['estado'] == 'Por preparar':
        print("Orden numero \n")
        print(order['id_pedido'])
        print("en preparacion")
        # Crea una lista de tareas para cada producto en el pedido
        tasks = []
        for product in order['productos']:
            match product['producto']:
                case 'Hamburguesa':
                    print("Toca preparar hamburgesa")
                    tasks.append(prepare_hamburgesa.s(order))
                case 'Pizza':
                    print("Toca preparar Pizza")
                    tasks.append(prepare_pizza.s(order))
                case 'Ensalada':
                    print("Toca preparar Ensaladas")
                    tasks.append(prepare_ensalada.s(order))
                case 'Refresco':
                    print("Toca sacar Refrescos")
                    tasks.append(prepare_refresco.s(order))
                case 'Agua':
                    print("Toca sacar agua")
                    tasks.append(prepare_agua.s(order))
                case 'Milanesa':
                    print("Toca preparar milanesas")
                    tasks.append(prepare_milanesa.s(order))
                case 'Papas fritas':
                    print("Toca preparar papas fritas")
                    tasks.append(prepare_papas_fritas.s(order))
                case 'Hot dog':
                    print("Toca preparar hots dogs")
                    tasks.append(prepare_hot_dog.s(order))
                case 'Tacos':
                    print("Toca preparar Tacos")
                    tasks.append(prepare_tacos.s(order))
                case _:
                    print("Producto no reconocido")

        print("Todas las ordenes pedidas\n")
        # Ejecuta todas las tareas en paralelo y luego ejecuta verify_order
        job = group(*tasks)
        results = job.apply_async()
        for result in results.results:
            while not result.state == 'SUCCESS':
                if result.state == 'PENDING':
                    print("Orden en espera")
                    time.sleep(5)

                elif result.state == 'STARTED':
                    print("Orden en proceso")
                    time.sleep(5)

                elif result.state == 'RETRY':
                    print("Reintentando la orden")
                    time.sleep(5)

                elif result.state == 'FAILURE':
                    print("Error en la preparacion de la orden")
                    return False

                elif result.state == 'SUCCESS':
                    print("Orden completada")
                    break

        # Verifica si todas las tareas han terminado
        if all(result.ready() for result in results.results):
            print("Resultados de la orden\n")
            if all(result.successful() for result in results.results):
                results = [result.result for result in results.results if result.ready()]
                if all(result for result in results):
                    order['estado'] = 'Completado'
                else:
                    order['estado'] = 'Error'
                return order

    else:
        print("No se puede preparar la orden debido a ingredientes insuficientes")
        order['estado'] = 'Error'
        return order
