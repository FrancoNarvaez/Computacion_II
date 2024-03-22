
---

# CLI-SERV App para Conexión Directa Cliente-Cocinero

La **CLI-SERV App** es una aplicación diseñada para facilitar la comunicación directa entre los clientes y los cocineros en un restaurante o local de comida,
eliminando la necesidad de un mozo intermediario. A través de esta aplicación, los clientes podrán acceder a un menú con diversas opciones y enviar sus pedidos
directamente al chef o chefs disponibles.

## Características Principales:

- **Menú Interactivo:** Los clientes podrán seleccionar los platos que deseen del menú, así como indicar las cantidades deseadas de cada uno.

- **Comunicación Directa:** La aplicación conecta directamente a los clientes con el chef o los chefs disponibles,
agilizando el proceso de pedido y reduciendo la dependencia de personal adicional.

- **Gestión de Pedidos:**
  - Los chefs recibirán las solicitudes de los clientes y las completarán según estén listas.
  - Los pedidos pueden ser cancelados por el chef en caso de algún inconveniente.

- **Gestión de Stock:**
  - Los chefs podrán modificar el estado de los platos en función del stock disponible o el horario de los platos por día 
  (por ejemplo, ciertos platos pueden estar disponibles solo para desayuno, almuerzo o cena).

- **Concurrencia y Paralelismo:**
  - Se implementa concurrencia para permitir que múltiples clientes envíen solicitudes al servidor simultáneamente.
  - Se utiliza paralelismo para manejar la situación donde hay más de un chef disponible, asignando a cada uno una lista de pedidos para preparar.

- **Tipos de Chefs:**
  - Se pueden definir distintos tipos de chefs para diferentes tareas, lo que permite que un pedido sea tomado por múltiples chefs según sea necesario.

¡La CLI-SERV App mejora la experiencia tanto para los clientes como para los cocineros, optimizando el proceso de pedido y preparación de alimentos en el local!

---
