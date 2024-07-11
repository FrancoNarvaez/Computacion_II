# Sistema de Gestión de Pedidos

Este proyecto implementa un sistema de gestión de pedidos para un restaurante, permitiendo verificar los ingredientes disponibles y preparar los pedidos según la demanda. Ahora, con soporte para Docker, Docker Compose e IPV4/IPV6 permitiendo la configuración y ejecución del proyecto de manera simplificada, facilitando su despliegue y pruebas.

## Características

- Verificación de ingredientes disponibles para cada pedido.
- Asignación de estados a los productos y pedidos según su disponibilidad y proceso de preparación.
- Ejecución de tareas de preparación de productos en paralelo utilizando Celery.
- Gestión de múltiples clientes y pedidos a través de hilos.
- Soporte para Docker y Docker Compose para una fácil configuración y despliegue.
- API consumible a través de Postman para pruebas y gestión de pedidos.

## Tecnologías Utilizadas

- Python: Lenguaje de programación principal.
- Celery: Biblioteca de Python para ejecutar tareas asíncronas distribuidas.
- Threading: Módulo de Python para ejecutar múltiples hilos de ejecución.
- Docker y Docker Compose: Para contenerizar y gestionar los componentes del proyecto.
- Postman: Para consumir y probar la API del proyecto.

## Configuración con Docker

Para ejecutar el proyecto utilizando Docker y Docker Compose, sigue estos pasos:

1. Asegúrate de tener Docker y Docker Compose instalados en tu sistema.
2. Asegúrate de tener corriendo el servicio de Docker y Docker-Compopose tu sistema.
2. Clona el repositorio del proyecto y navega hasta la carpeta del mismo.
3. Ejecuta `docker-compose up --build` para construir y levantar los contenedores de Flask y Celery.

Esto iniciará todos los servicios necesarios para el proyecto, incluyendo la base de datos y cualquier otro servicio definido en tu `docker-compose.yml`.

## Uso con Postman

Para consumir la API del proyecto con Postman:

1. Asegúrate de que los contenedores de Docker estén corriendo.
2. Abre Postman y configura una nueva petición apuntando a la URL del servicio Flask, por ejemplo, `http://localhost:8080/api/pedidos`.
3. Configura el método HTTP adecuado (GET, POST, etc.) y añade cualquier dato necesario en el cuerpo de la petición para simular un pedido.
4. Envía la petición y observa la respuesta de la API para verificar el estado del pedido o cualquier otra información relevante.