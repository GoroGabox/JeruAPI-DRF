# API de Restaurante

Esta API de Restaurante se ha desarrollado utilizando Django Rest Framework (DRF) y proporciona endpoints para gestionar diversas entidades relacionadas con un restaurante, como usuarios, roles, ingredientes, productos, pedidos y más. Esta documentación proporciona una visión general de la API y cómo utilizarla.

## Contenido

1. [Requisitos](#requisitos)
2. [Instalación](#instalación)
3. [Ejecución](#ejecución)
4. [Endpoints](#endpoints)
5. [Ejemplos de Uso](#ejemplos-de-uso)
6. [Autorización](#autorización)
7. [Contribuciones](#contribuciones)

## Requisitos

Asegúrate de tener instalados los siguientes componentes antes de comenzar:

- Python (3.6 o superior)
- Django (3.0 o superior)
- Django Rest Framework (3.0 o superior)

## Instalación

1. Clona este repositorio en tu máquina local:

```bash
git clone https://github.com/tuusuario/restaurante-api.git
```

2. Navega al directorio del proyecto:

```bash
cd restaurante-api
```

3. Crea un entorno virtual (recomendado) y actívalo:

```bash
python -m venv venv
source venv/bin/activate  # En Windows, usa `venv\Scripts\activate`
```

4. Instala las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

## Ejecución

1. Asegúrate de que estás en el directorio raíz del proyecto y ejecuta el servidor de desarrollo:

```bash
python manage.py runserver
```

2. La API estará disponible en `http://localhost:8000/`.

## Endpoints

La API proporciona los siguientes endpoints para gestionar las entidades:

- `/api/accounts/register/`: Endpoint para registrar usuarios.
- `/api/accounts/login/`: Endpoint para autenticar usuario.
- `/api/accounts/token/refresh/`: Endpoint para refrescar token de acceso.
- `/api/accounts/logout/`: Endpoint para desautenticar usuario.
- `/api/accounts/roles/`: Endpoint para gestionar roles de usuarios.
- `/api/accounts/usuarios/`: Endpoint para gestionar usuarios.
- `/api/restaurant/ingredientes/`: Endpoint para gestionar ingredientes.
- `/api/restaurant/categorias/`: Endpoint para gestionar categorías de productos.
- `/api/restaurant/productos/`: Endpoint para gestionar productos.
- `/api/restaurant/productos-ingredientes/`: Endpoint para gestionar la relación entre productos e ingredientes.
- `/api/restaurant/pedidos/`: Endpoint para gestionar pedidos.
- `/api/restaurant/pedidos-productos/`: Endpoint para gestionar la relación entre pedidos y productos.

## Ejemplos de Uso

A continuación, se muestran algunos ejemplos de cómo utilizar la API:

- **Crear un nuevo usuario:**

  ```bash
  POST /api/accounts/register/
  {
      "nombre": "Juan",
      "apellido": "Perez",
      "nombre_usuario": "juanperez",
      "contraseña": "micontraseña",
      "rol": 1  # ID del rol
  }
  ```

- **Obtener todos los productos:**

  ```bash
  GET /productos/
  ```

- **Actualizar un pedido:**

  ```bash
  PUT /pedidos/1/
  {
      "estado": "Entregado"
  }
  ```

- **Eliminar un ingrediente:**

  ```bash
  DELETE /ingredientes/2/
  ```

## Autorización

Para acceder a ciertos endpoints, es posible que se requiera autorización. Asegúrate de configurar la autenticación y los permisos de acuerdo con tus necesidades. Consulta la documentación de Django Rest Framework para obtener más detalles sobre la autenticación y la autorización.

## Contribuciones

¡Las contribuciones son bienvenidas! Si deseas mejorar esta API o solucionar problemas, no dudes en enviar un Pull Request. Por favor, sigue las mejores prácticas de desarrollo y asegúrate de que todas las pruebas pasen antes de enviar tus cambios.