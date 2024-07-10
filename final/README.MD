# Sistema de Gestión de Pedidos

Este proyecto implementa un sistema de gestión de pedidos para un restaurante, permitiendo verificar los ingredientes disponibles y preparar los pedidos según la demanda.

## Características

- Verificación de ingredientes disponibles para cada pedido.
- Asignación de estados a los productos y pedidos según su disponibilidad y proceso de preparación.
- Ejecución de tareas de preparación de productos en paralelo utilizando Celery.
- Gestión de múltiples clientes y pedidos a través de hilos.

## Tecnologías Utilizadas

- Python: Lenguaje de programación principal.
- Celery: Biblioteca de Python para ejecutar tareas asíncronas distribuidas.
- Threading: Módulo de Python para ejecutar múltiples hilos de ejecución.

## Estructura del Proyecto

- `app/clients.py`: Gestiona la comunicación con los clientes y el envío de pedidos.
- `app/task.py`: Define las tareas de verificación de ingredientes y preparación de pedidos.
- `app/despensa.py`: Almacena la información sobre los ingredientes disponibles.
- `app/celery_app.py`: Configura la aplicación Celery para la ejecución de tareas asíncronas.

## Configuración

1. Instalar las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

2. Ejecutar el servidor de Redis:

```bash
redis-server
```

3. Ejecutar el servidor de Celery:

```bash
celery -A app.celery_app worker --loglevel=info
```

4. Ejecutar el script principal:

```bash
python run.py
```

## Uso

1. Iniciar el servidor y esperar a que los clientes realicen pedidos.
2. Verificar cómo se procesan los pedidos y se preparan los productos en paralelo.
3. Observar cómo se actualiza el estado de los pedidos y productos según su disponibilidad.
4. Finalizar la ejecución del programa con `Ctrl + C`.
5. Verificar que no hayan tareas pendientes en el servidor de Celery.
6. Cerrar el servidor de Redis.
7. Finalizar la ejecución del programa.
8. ¡Listo!

