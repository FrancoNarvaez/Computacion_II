from flask import jsonify, request
from app.order import Order
from app.task import check_ingredients, prepare
from celery import chain
import uuid
from app.celery_app import app as celery_app


def init_app(app):
    @app.route('/menu', methods=['GET'])
    def get_menu():
        menu = {
            'productos': [
                {'nombre': 'Hamburguesa', 'precio': 5},
                {'nombre': 'Pizza', 'precio': 4},
                {'nombre': 'Ensalada', 'precio': 2},
                {'nombre': 'Refresco', 'precio': 1},
                {'nombre': 'Agua', 'precio': 1},
                {'nombre': 'Milanesa', 'precio': 5},
                {'nombre': 'Papas fritas', 'precio': 2},
                {'nombre': 'Hot dog', 'precio': 3},
                {'nombre': 'Tacos', 'precio': 5}
            ]
        }
        return jsonify(menu)

    @app.route('/status/<task_id>', methods=['GET'])
    def get_status(task_id):
        try:
            result = celery_app.AsyncResult(task_id)
            if result.ready():
                task_result = result.result
                return jsonify(task_result)
            else:
                return jsonify({"status": result.state})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/pedido', methods=['POST'])
    def create_order():
        params = request.json
        id_pedido = str(uuid.uuid4())
        params['id_pedido'] = id_pedido
        order = Order(params)
        workflow = chain(check_ingredients.s(order.order_dict), prepare.s())
        result = workflow.delay()
        return jsonify({"task_id": result.id})
