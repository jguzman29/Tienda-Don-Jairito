# Tienda de Don Jairito - Python & MySQL

Simulador de un sistema de punto de venta (POS) para una tienda de barrio, integrado con base de datos MySQL mediante el ORM SQLAlchemy.

## Funcionalidades

* **Gestión de Clientes:** Búsqueda y registro automático de clientes en MySQL por cédula.
* **Inventario Dinámico:** Base de datos relacional con 20 productos de abarrotes.
* **Carrito de Compras:** Cálculo automático de subtotales, totales y registro de detalle de venta.
* **Generación de Tiquete:** Muestra los datos del cliente, productos comprados, pago y devueltos.
* **Persistencia de Datos:** Guardado relacional en MySQL de clientes, ventas y detalle de ventas.
* **Manejo de Excepciones:** Validaciones para entradas de números y control de errores en la base de datos.

## Tecnologías Usadas

* **Lenguaje:** Python 3
* **ORM:** SQLAlchemy
* **Base de Datos:** MySQL
* **Conector:** PyMySQL / mysql-connector-python

## Estructura del Proyecto

* `estructuras.py`: Define los modelos ORM (Cliente, Producto, Venta, DetalleVenta) y maneja la conexión a MySQL.
* `main.py`: Lógica principal e interactiva del punto de venta.

## Autor

Desarrollado por **Juan Diego** como parte de mi formación técnica y universitaria en programación.