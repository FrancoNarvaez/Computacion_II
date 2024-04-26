from celery import group
import time
from despensa import ingredientes
from celery.result import AsyncResult
from configRedis import app


class Order:
    def __init__(self, order_dict):
        self.order_dict = order_dict

    @app.task
    def check_ingredients(self):
        # Verifica si hay suficientes ingredientes para cada producto en el pedido
        for producto_dict in self.order_dict['productos']:
            producto = producto_dict['producto']
            cantidad = producto_dict['cantidad']
            # Si no hay suficientes ingredientes para un producto, establece el estado a 'Insuficiente'
            if ingredientes[producto] < cantidad:
                self.order_dict['estado'] = 'Insuficiente'
                print("Soy el order en check_ingredientes:\n", self.order_dict, "\nNo hay sufiencientes ingredientes")
                return self.order_dict

        # Si hay suficientes ingredientes para todos los productos, establece el estado a 'En proceso'
        self.order_dict['estado'] = 'Por preparar'
        return self.order_dict

    @app.task
    def prepare(self, product_to_function):
        print("voy a prepara la orden")
        if self.order_dict['estado'] == 'Por preparar':
            print("Orden numero \n")
            print(self.order_dict['id_pedido'])
            print("en preparacion")
            # Crea una lista de tareas para cada producto en el pedido
            tasks = []
            for product in self.order_dict['productos']:
                prepare_function = product_to_function.get(product['producto'])
                if prepare_function:
                    print(f"Toca preparar {product['producto']}")
                    tasks.append(prepare_function.s(product))  # Aquí pasamos solo el producto
                else:
                    print("Producto no reconocido")

            print("Todas las ordenes pedidas\n")
            # Ejecuta todas las tareas en paralelo
            job = group(*tasks)
            results = job.apply_async()

            # Recoge los estados de los productos de las tareas
            for result in results.results:
                result_id = result.id
                while result.state != 'SUCCESS':
                    time.sleep(1)  # Espera un poco antes de revisar de nuevo
                product_name, product_status = result.result
                # Actualiza el estado del producto en la orden
                for product in self.order_dict['productos']:
                    if product['producto'] == product_name:
                        product['estado'] = product_status
                        break

            # Verifica si todos los productos están completados
            if all(product.get('estado') == 'Completado' for product in self.order_dict['productos']):
                self.order_dict['estado'] = 'Completado'
            else:
                self.order_dict['estado'] = 'Error'

            return self.order_dict

    def update_order_status(self, task_id):
        # Obtiene el estado de la tarea
        result = AsyncResult(task_id)
        self.order_dict['estado'] = result.state
        return self.order_dict
