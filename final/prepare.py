import time


def prepare_ensalada(product):
    time.sleep(5)
    if product['producto'] == 'Ensalada':
        print("Ensalada preparada")
        product['estado'] = 'Completado'
        print('En ensalada\nProducto saliente:', product)
        return product['producto'], product['estado']


def prepare_hamburguesa(product):
    time.sleep(15)
    if product['producto'] == 'Hamburguesa':
        print("Hamburguesa preparada")
        product['estado'] = 'Completado'
        print('En hamburgesa\nOrden saliente:', product)
        return product['producto'], product['estado']


def prepare_pizza(product):
    time.sleep(5)
    if product['producto'] == 'Pizza':
        print("Pizza preparada")
        product['estado'] = 'Completado'
        print('En pizza\nOrden saliente:', product)
        return product['producto'], product['estado']


def prepare_refresco(product):
    time.sleep(5)
    if product['producto'] == 'Refresco':
        print("Refresco preparado")
        product['estado'] = 'Completado'
        return product['producto'], product['estado']


def prepare_agua(product):
    time.sleep(5)
    if product['producto'] == 'Agua':
        print("Agua preparada")
        product['estado'] = 'Completado'
        return product['producto'], product['estado']


def prepare_milanesa(product):
    time.sleep(5)
    if product['producto'] == 'Milanesa':
        print("Milanesa preparada")
        product['estado'] = 'Completado'
        return product['producto'], product['estado']


def prepare_papas_fritas(product):
    time.sleep(5)
    if product['producto'] == 'Papas fritas':
        print("Papas fritas preparadas")
        product['estado'] = 'Completado'
        return product['producto'], product['estado']


def prepare_hot_dog(product):
    time.sleep(5)
    if product['producto'] == 'Hot dog':
        print("Hot dog preparado")
        product['estado'] = 'Completado'
        return product['producto'], product['estado']


def prepare_tacos(product):
    time.sleep(5)
    if product['producto'] == 'Tacos':
        print("Tacos preparados")
        product['estado'] = 'Completado'
        return product['producto'], product['estado']