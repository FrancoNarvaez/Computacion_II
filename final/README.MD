# Sistema de Gestión de Pedidos

Este proyecto implementa un sistema de gestión de pedidos para un restaurante, permitiendo verificar los ingredientes disponibles y preparar los pedidos según la demanda. Utiliza Docker y Docker Compose para facilitar la configuración, despliegue y pruebas, con soporte para IPv4 e IPv6.

## Características

- Verificación de ingredientes disponibles para cada pedido.
- Asignación de estados a los productos y pedidos.
- Ejecución paralela de tareas de preparación utilizando Celery.
- Gestión de múltiples clientes y pedidos.
- API RESTful para la gestión de pedidos.
- Soporte para IPv4 e IPv6.

## Tecnologías Utilizadas

- Python: Lenguaje de programación principal.
- Flask: Framework web para crear la API RESTful.
- Celery: Para tareas asíncronas distribuidas.
- Redis: Como broker de mensajes para Celery y almacenamiento de resultados.
- Gunicorn: Servidor WSGI HTTP para ejecutar la aplicación Flask en producción.
- Docker y Docker Compose: Para contenerización y orquestación de servicios.
- Postman: Para pruebas de la API.

## Configuración y Ejecución

1. Asegúrate de tener Docker y Docker Compose instalados.
2. Clona el repositorio y navega hasta la carpeta del proyecto.
3. Ejecuta:

```bash
docker-compose down --volumes
docker-compose up --build
```
Esto iniciará todos los servicios necesarios para el proyecto.

## Uso de la API

Puedes usar Postman o curl para interactuar con la API:

1. Obtener el menú:

```bash
curl http://localhost:8080/menu
```
2. Crear un pedido:

```bash
curl -X POST http://localhost:8080/pedido -H "Content-Type: application/json" -d '{"productos": [{"producto": "Hamburguesa", "cantidad": 1}]}' 
```
3. Verificar el estado de un pedido:

```bash
curl http://localhost:8080/status/<task_id>
```

Reemplaza `<task_id>` con el ID devuelto al crear el pedido.

## Soporte IPv6

Para usar IPv6, simplemente reemplaza `localhost` con `[::1]` en las URLs de la API.

## Uso con Postman

Para consumir la API del proyecto con Postman:

1. Abre Postman y configura una nueva petición apuntando a la URL del servicio Flask, por ejemplo, `http://[::1]:8080/menu` para IPV6 o `http://localhost:8080/menu` para IPV4.
2. Configura el método HTTP adecuado (GET, POST, etc.) y añade cualquier dato necesario en el cuerpo de la petición para simular un pedido.
3. Envía la petición y observa la respuesta de la API para verificar el estado del pedido o cualquier otra información relevante.
