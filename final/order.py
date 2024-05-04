from celery.result import AsyncResult


class Order:
    def __init__(self, order_dict):
        self.order_dict = order_dict

    def update_order_status(self, task_id):
        # Obtiene el estado de la tarea
        result = AsyncResult(task_id)
        self.order_dict['estado'] = result.state
        return self.order_dict
