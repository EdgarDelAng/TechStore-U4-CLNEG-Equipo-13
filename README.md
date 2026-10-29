# TechStore · Actividad 4

**Actividad Práctica 4 · Componentes de Lógica de Negocio · Unidad 4**

TechStore es un proyecto desarrollado en Python para administrar pedidos de una tienda ficticia. La aplicación implementa el núcleo de negocio de los pedidos: entidades y objetos de valor, reglas de descuento, validaciones, control de estados, Domain Events y una API REST con FastAPI. El comportamiento se verifica mediante los escenarios E01–E15 y pruebas automatizadas con pytest.

## Datos de la actividad

| Dato | Información |
|---|---|
| **Proyecto** | TechStore |
| **Actividad** | Actividad Práctica 4 |
| **Materia** | Componentes de Lógica de Negocio |
| **Lenguaje** | Python 3.11 o superior |
| **API** | FastAPI |
| **Pruebas** | pytest |
| **Repositorio** | Agregar aquí la URL del repositorio de GitHub |

> Los datos de grupo, profesor e integrantes pueden agregarse aquí cuando se confirme la información de entrega.

## Descripción

El proyecto carga clientes, productos y pedidos desde archivos CSV y los convierte en objetos que utiliza el dominio. A partir de esos datos, PetMarket permite evaluar descuentos, validar las condiciones de los pedidos y ejecutar operaciones de su ciclo de vida mediante una API.

La lógica del negocio se mantiene separada de la API. De esta forma, las reglas del dominio pueden probarse con pytest y con los escenarios definidos para la actividad, además de ejecutarse mediante solicitudes HTTP desde Swagger UI.

## Contenido del proyecto

| Carpeta o archivo | Descripción |
|---|---|
| `app/domain.py` | Entidades, Value Objects, validaciones, estados y eventos de dominio. |
| `app/specifications.py` | Specifications que representan las reglas de descuento. |
| `app/service.py` | Servicio que coordina las operaciones sobre los pedidos. |
| `app/api.py` | Endpoints REST y respuestas de la API con FastAPI. |
| `datos/` | Archivos CSV de clientes, productos, pedidos y escenarios. |
| `tests/` | Pruebas del dominio, Specifications, datos, escenarios y API. |
| `evidencias/` | Capturas de ejecución y bitácora de los escenarios. |
| `cargar_csv.py` | Lee los CSV y prepara los objetos del proyecto. |
| `ejecutar_escenarios.py` | Ejecuta los escenarios E01–E15. |
| `requirements.txt` | Dependencias requeridas. |
| `pytest.ini` | Configuración de pytest. |

## Estado de validación

Los resultados documentados para el proyecto son:

- **Pruebas automatizadas:** `232 passed`.
- **Escenarios:** `15/15` cumplen su objetivo (E01–E15).
- **Carga de datos:** 16 pedidos.
- **API:** disponible mediante Uvicorn y documentada con Swagger UI.

Estos resultados corresponden a las ejecuciones registradas del proyecto. Si se modifica el código o el entorno, es recomendable volver a ejecutar las comprobaciones.

## Requisitos

- Python 3.11 o superior.
- PowerShell o una terminal compatible.
- Conexión a Internet para instalar las dependencias.

## Instalación en Windows PowerShell

Abre la carpeta raíz del proyecto `PetMarket_U4` en VS Code. Desde la terminal, ejecuta:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

No es obligatorio activar el entorno virtual si se utiliza directamente el ejecutable `.\.venv\Scripts\python.exe`, como en los comandos de este README. Si prefieres activarlo:

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación, puedes continuar utilizando el ejecutable del entorno virtual.

## Carga de datos

Los archivos de entrada se encuentran en `datos/`. Para procesarlos y cargar los pedidos, ejecuta:

```powershell
.\.venv\Scripts\python.exe cargar_csv.py
```

El proyecto utiliza 16 pedidos que se encuentran definidos en los archivos CSV.

## Ejecutar los escenarios E01–E15

Para ejecutar los escenarios en modo normal:

```powershell
.\.venv\Scripts\python.exe ejecutar_escenarios.py
```

Para mostrar el detalle y generar o actualizar la bitácora:

```powershell
.\.venv\Scripts\python.exe ejecutar_escenarios.py --bitacora
```

El resultado esperado es que los 15 escenarios cumplan su objetivo. La bitácora se encuentra en `evidencias/bitacora_escenarios.md`.

## Ejecutar las pruebas automatizadas

Desde la carpeta raíz del proyecto:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

La ejecución documentada reportó `232 passed`. Si se realizan cambios al código, vuelve a ejecutar pytest para verificar que las pruebas continúen pasando.

## Iniciar la API REST

Ejecuta Uvicorn desde la raíz del proyecto:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.api:app --host 127.0.0.1 --port 8000
```

Con el servidor activo, abre:

- **Swagger UI:** <http://127.0.0.1:8000/docs>
- **Esquema OpenAPI:** <http://127.0.0.1:8000/openapi.json>

Para detener el servidor, regresa a la terminal y presiona `Ctrl+C`. Si el puerto 8000 está ocupado, puedes iniciar la API en el puerto 8001 y abrir `http://127.0.0.1:8001/docs`.

La aplicación mantiene los pedidos en memoria. Los cambios realizados mediante la API se pierden al reiniciar Uvicorn y los datos vuelven a cargarse desde los CSV.

## Reglas de negocio

### Descuentos

Las reglas de descuento se encuentran en `app/specifications.py`.

| Descuento | Condiciones |
|---|---|
| **10 % · VIP** | El cliente es VIP, el total es mayor a $500 MXN, el pedido suma al menos 4 unidades y no tiene una promoción activa. |
| **5 % · Importe alto** | El total es mayor a $5,000 MXN y no existe una promoción activa. |
| **0 %** | No se cumple ninguna de las condiciones anteriores. |

Si se cumplen ambas reglas, se aplica el descuento del 10 %. Evaluar el descuento no modifica el total original del pedido; el importe descontado y el total final se calculan por separado.

### Dinero, artículos y límite de unidades

- `Money` representa importes mediante `Decimal` y no admite cantidades negativas ni valores no finitos.
- `Customer` representa al cliente y conserva las condiciones de cliente VIP y activo.
- `OrderItem` representa un artículo mediante su SKU, cantidad y precio unitario; también calcula el subtotal.
- Cada pedido admite como máximo **20 unidades en total**. Se suman las cantidades de los artículos, no el número de renglones.
- Si una operación excede el límite, se rechaza sin modificar los artículos del pedido.
- Los artículos solo pueden agregarse mientras el pedido está en `DRAFT`.
- La existencia del catálogo se conserva como información del producto; esta actividad no requiere descontar inventario.

## Estados y Domain Events

Los pedidos comienzan en `DRAFT`. Las transiciones permitidas son:

| Estado inicial | Operación | Estado final | Domain Event | Condición |
|---|---|---|---|---|
| `DRAFT` | `confirm()` | `CONFIRMED` | `OrderConfirmed` | El pedido contiene artículos y el cliente está activo. |
| `CONFIRMED` | `ship(tracking_number)` | `SHIPPED` | `OrderShipped` | La guía no está vacía. |
| `CONFIRMED` | `cancel(reason)` | `CANCELLED` | `OrderCancelled` | El motivo no está vacío. |
| `SHIPPED` | `deliver()` | `DELIVERED` | `OrderDelivered` | El pedido se encuentra en `SHIPPED`. |
| `SHIPPED` | `return_order()` | `RETURNED` | `OrderReturned` | El pedido se encuentra en `SHIPPED`. |

`DELIVERED`, `RETURNED` y `CANCELLED` son estados finales. Los eventos representan hechos que ya ocurrieron y se registran después de completar una transición válida. Si una operación se rechaza, el estado del pedido no cambia y no se agrega el evento correspondiente.

## API REST

La API se encuentra en `app/api.py`. Las rutas disponibles se pueden consultar desde Swagger UI (`/docs`) al iniciar el servidor. Entre las operaciones del sistema se encuentran:

- Consultar la lista de pedidos.
- Consultar un pedido por su identificador.
- Confirmar un pedido.
- Enviar un pedido con número de guía.
- Cancelar un pedido con motivo.
- Registrar la entrega de un pedido enviado.
- Registrar la devolución de un pedido enviado.

### Respuestas HTTP

| Código | Significado |
|---|---|
| `200` | Consulta u operación realizada correctamente. |
| `404` | El pedido solicitado no existe. |
| `409` | La operación no está permitida desde el estado actual. |
| `422` | Los datos o las condiciones de negocio no son válidos; también puede indicar que se excedió el límite de unidades. |

Las respuestas de error permiten identificar el tipo de problema y el mensaje correspondiente. Las operaciones que no se completan no deben cambiar el estado ni registrar el evento de una transición que no ocurrió.

## Demostración rápida

Desde la carpeta `PetMarket_U4`, ejecuta:

```powershell
.\.venv\Scripts\python.exe cargar_csv.py
.\.venv\Scripts\python.exe ejecutar_escenarios.py
.\.venv\Scripts\python.exe -m pytest -q
```

Después, inicia Uvicorn y abre Swagger UI en `/docs` para consultar pedidos y probar las operaciones disponibles. Para volver a comenzar con los datos originales, detén el servidor y vuelve a ejecutar la carga o inicia de nuevo la aplicación.

## Evidencias

La carpeta `evidencias/` contiene capturas de la carga de datos, la ejecución de escenarios, las pruebas automatizadas y las respuestas de la API. También se conserva la bitácora de escenarios para relacionar cada caso con sus precondiciones, operación y resultado.

## Repositorio

**GitHub:** [Agregar aquí la URL del repositorio PetMarket]

---

**PetMarket · Actividad 4 · Componentes de Lógica de Negocio**
