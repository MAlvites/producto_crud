# productos_crud
## API para la gestión de productos

Este proyecto proporciona una API para manejar un inventario de productos con funcionalidades de crear, leer, actualizar y eliminar (CRUD). Los productos se almacenan en un archivo JSON y se pueden gestionar a través de una interfaz web.

## Endpoints

### Lista de Productos
- **URL**: `/`
- **Descripción**: Muestra la lista de productos almacenados en el archivo JSON. Permite filtrar productos por precio y categoría, y paginarlos.
- **Parámetros de Consulta**:
  - `min_price`: Precio mínimo para filtrar productos (opcional).
  - `max_price`: Precio máximo para filtrar productos (opcional).
  - `categoria`: Categoría para filtrar productos (opcional).
  - `page`: Número de página para paginación (opcional, valor predeterminado 1).
  - `size`: Número de productos por página (opcional, valor predeterminado 10).

### Crear Producto
- **URL**: `/crear`
- **Descripción**: Muestra un formulario para crear un nuevo producto.
- **Parámetros del Formulario**:
  - `nombre`: Nombre del producto.
  - `categoría`: Categoría del producto.
  - `precio`: Precio del producto (debe ser mayor que 0).
  - `stock`: Cantidad en stock (no puede ser negativo).

### Guardar Producto
- **URL**: `/crear/guardar`
- **Descripción**: Guarda un nuevo producto en el archivo JSON.

### Actualizar Producto
- **URL**: `/{id}/actualizar`
- **Descripción**: Muestra un formulario para actualizar un producto existente.
- **Parámetros del Formulario**:
  - `nombre`: Nombre del producto.
  - `categoría`: Categoría del producto.
  - `precio`: Precio del producto (debe ser mayor que 0).
  - `stock`: Cantidad en stock (no puede ser negativo).


### Guardar Actualización
- **URL**: `/{id}/actualizar/guardar`
- **Descripción**: Guarda los cambios realizados en un producto.


### Eliminar Producto
- **URL**: `/{id}/eliminar`
- **Método**: `POST`
- **Descripción**: Elimina un producto específico.
- **Parámetros**:
  - `id`: ID del producto a eliminar.

## Correr la Aplicación

1. Clona el repositorio con el siguiente comando:
   git clone https://github.com/MAlvites/productos_crud.git
2. Ejecutar el siguiente comando en la carpeta del repositorio
    uvicorn app:app --reload