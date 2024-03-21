from celery import Celery
# Luego crear para conectar con el servidor, realizando un get de la url necesaria para la lista de pedidos, cuando la cree.
app = Celery('tasks', broker='pyamqp://guest@localhost//')


@app.task
def prepare_order(order):
    pass
