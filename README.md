# Sistema de Lavandería

Repositorio para la asignatura de Programación Orientada a Objetos Seguro.

**Profesor:** Michael Arjel  
**Institución:** Inacap  
**Alumnos:** Francisco Lara, Genesis Sepúlveda  

---

## Descripción del Proyecto

Sistema modular orientado a objetos para la gestión integral de un negocio de **Lavandería**.

El sistema aplica buenas prácticas de diseño de software y principios fundamentales de la Programación Orientada a Objetos:
* **Encapsulamiento estricto:** Atributos privados (`__atributo`), validación de integridad mediante propiedades `@property` y decoradores setter.
* **Herencia y Polimorfismo:** Jerarquías de clases para personal (`Empleado` -> `Cajero`, `Operario`) y prendas (`Prenda` -> `RopaNormal`, `Alfombra`, `EdredonCobertor`), con cálculo dinámico de costos y tiempos de ciclo según tipo de prenda y tratamiento.
* **Separación de Responsabilidades (Capa DAO):** Capa de acceso a datos relacional SQLite (`lavanderia.db`) que abstrae las operaciones de persistencia mediante especialización de la clase base `DAO`.
* **Manejo de Moneda Extranjera:** Conversión de insumos químicos en dólares (USD) a pesos chilenos (CLP) en base a `CotizacionDolar`.

---

## Estructura del Repositorio

```text
Lavanderia/
│
├── conectar.py               # Gestión de conexión SQLite (lavanderia.db) con PRAGMA foreign_keys
├── main.py                   # Script de integración, generación de tablas y pruebas de dominio
├── README.md                 # Documentación técnica del sistema y bitácora de avances
├── .gitignore                # Reglas de exclusión de archivos temporales y compilados
├── lavanderia.db             # Base de datos relacional SQLite
│
├── dao/                      # Capa de Acceso a Datos (Data Access Object)
│   ├── __init__.py
│   ├── dao.py                # Clase base DAO
│   ├── cliente_dao.py
│   ├── empleado_dao.py
│   ├── cajero_dao.py
│   ├── operario_dao.py
│   ├── maquina_dao.py
│   ├── producto_quimico_dao.py
│   ├── cotizacion_dolar_dao.py
│   ├── prenda_dao.py
│   ├── ropa_normal_dao.py
│   ├── alfombra_dao.py
│   ├── edredon_cobertor_dao.py
│   ├── orden_dao.py
│   └── detalle_orden_dao.py
│
└── model/                    # Capa de Dominio (Modelos POO)
    ├── __init__.py
    ├── cliente.py
    ├── empleado.py           # Clase abstracta base
    ├── cajero.py
    ├── operario.py
    ├── maquina.py
    ├── cotizacion_dolar.py
    ├── producto_quimico.py
    ├── prenda.py             # Clase abstracta base
    ├── ropa_normal.py
    ├── alfombra.py
    ├── edredon_cobertor.py
    ├── detalle_orden.py
    └── orden.py
```

---

## Bitácora de Avances

### 15 de Septiembre de 2026
- **Inicialización del Proyecto:** Creación de la estructura del repositorio de trabajo y archivo `.gitignore` para exclusión de archivos compilados de Python.
- **Creación de Clase `CotizacionDolar` (`model/cotizacion_dolar.py`):**
  - Implementación del constructor con atributos privados `__fecha` y `__valor_dolar`.
  - Validación de valor positivo mediante decorador `@valor_dolar.setter`.
  - Definición del método `obtenerValorDolar()` para consulta de la tasa de cambio.
- **Creación de Clase `ProductoQuimico` (`model/producto_quimico.py`):**
  - Definición de atributos privados `__nombre` y `__precio_dolar` con validaciones de texto no vacío y monto no negativo.
  - Implementación del método de negocio `calcularPrecioPesos(valorDolar)` para convertir el costo unitario de insumos a moneda nacional (CLP).

### 17 de Septiembre de 2026
- **Creación de Clase `Cliente` (`model/cliente.py`):**
  - Encapsulamiento del atributo privado `__rut`.
  - Validación de formato mediante expresión regular en el setter.
  - Implementación del método `validarRut()` con el algoritmo completo de verificación de dígito verificador chileno.
- **Creación de Clase `Maquina` (`model/maquina.py`):**
  - Atributo privado `__id_maquina` validado para enteros positivos.
  - Implementación del método `iniciarLavado()` que simula el inicio operativo del ciclo del equipo.

### 21 de Septiembre de 2026
- **Creación de Clase Abstracta `Empleado` (`model/empleado.py`):**
  - Clase base que hereda de `abc.ABC` con atributo privado `__id_empleado` y propiedades de lectura.
- **Implementación de Subclase `Cajero` (`model/cajero.py`):**
  - Hereda de `Empleado` e invoca al constructor superior mediante `super().__init__(id_empleado)`.
  - Implementación de métodos de atención y recaudación: `recibirPrendas()`, `registrarOrden()`, `cobrarOrden()` y `entregarPrendas()`.
- **Implementación de Subclase `Operario` (`model/operario.py`):**
  - Hereda de `Empleado` con atributo privado `__maquinas_asignadas` tipo lista.
  - Implementación de métodos de gestión de planta: `asignar_maquina()`, `procesarPrenda()` y `operarMaquina()`.

### 23 de Septiembre de 2026
- **Creación de Clase Abstracta `Prenda` (`model/prenda.py`):**
  - Definición de atributos privados `__estado_inicial`, `__lavado_seco` y relación de composición con `ProductoQuimico`.
  - Método `validarEstado()` para comprobar si la prenda es apta para proceso.
  - Declaración de métodos abstractos polimórficos `@abstractmethod def calcularCosto()` y `@abstractmethod def calcularTiempoLavado()`.
- **Implementación de Subclases de Prendas:**
  - **`RopaNormal` (`model/ropa_normal.py`):** Sobrescritura de `calcularCosto()` con tarifa base y recargo por lavado en seco; y `calcularTiempoLavado()` con tiempos estándar.
  - **`Alfombra` (`model/alfombra.py`):** Sobrescritura de `calcularCosto()` para lavado pesado de fibras y `calcularTiempoLavado()` para ciclo extendido.
  - **`EdredonCobertor` (`model/edredon_cobertor.py`):** Sobrescritura de `calcularCosto()` adaptado a piezas de gran volumen y duración de ciclo especializada.

### 26 de Septiembre de 2026
- **Creación de Clase `DetalleOrden` (`model/detalle_orden.py`):**
  - Atributos privados `__prenda` y `__cantidad` (con validación de entero mayor a 0).
  - Implementación de `calcularSubtotal()` multiplicando el costo unitario polimórfico de la prenda por la cantidad solicitada.
- **Creación de Clase `Orden` (`model/orden.py`):**
  - Consolidación de atributos privados: `__num_orden`, `__num_boleta`, `__cliente`, `__cajero`, `__detalles` y `__pagada`.
  - Implementación de métodos transaccionales:
    - `validarIdentificacion()`: Comprobación de existencia de cliente y cajero junto con validación del RUT.
    - `calcularTotal()`: Sumatoria acumulativa de subtotales de la lista de detalles.
    - `verificarPago()`: Verificación del estado booleano de pago.
    - `entregarOrden()`: Control seguro de despacho, impidiendo entregas sin pago previo.

### 29 de Septiembre de 2026
- **Conexión de Base de Datos (`conectar.py` y `lavanderia.db`):**
  - Implementación de la función `crear_conexion()` conectando a `lavanderia.db`.
  - Activación obligatoria de integridad referencial relacional mediante `PRAGMA foreign_keys = ON`.
- **Diseño de la Capa DAO (`dao/`):**
  - Creación del paquete `dao/` e inicialización con `__init__.py`.
  - Creación de la clase base `DAO` (`dao/dao.py`) con inyección de conexión y cursor de SQLite.
  - Creación de DAOs para tablas maestras independientes:
    - `ClienteDAO` (`dao/cliente_dao.py`): Definición y creación de tabla `cliente`.
    - `EmpleadoDAO` (`dao/empleado_dao.py`): Creación de tabla base `empleado`.
    - `MaquinaDAO` (`dao/maquina_dao.py`): Creación de tabla de equipos `maquina`.
    - `ProductoQuimicoDAO` (`dao/producto_quimico_dao.py`): Creación de tabla `producto_quimico`.
    - `CotizacionDolarDAO` (`dao/cotizacion_dolar_dao.py`): Creación de tabla `cotizacion_dolar`.

### 2 de Octubre de 2026
- **Especialización de DAOs Relacionales con Herencia y Claves Foráneas:**
  - Implementación de `CajeroDAO` (`dao/cajero_dao.py`) y `OperarioDAO` (`dao/operario_dao.py`) heredando de `EmpleadoDAO` con relación foránea a `empleado`.
  - Implementación de `PrendaDAO` (`dao/prenda_dao.py`) con clave foránea a `producto_quimico`.
  - Implementación de `RopaNormalDAO`, `AlfombraDAO` y `EdredonCobertorDAO` extendiendo de `PrendaDAO`.
  - Implementación de `OrdenDAO` (`dao/orden_dao.py`) y `DetalleOrdenDAO` (`dao/detalle_orden_dao.py`) con relaciones foráneas a clientes, cajeros, órdenes y prendas.

### 4 de Octubre de 2026
- **Integración General y Pruebas del Sistema (`main.py`):**
  - Desarrollo del script principal `main.py` que instancia todos los DAOs y ejecuta la creación automática de tablas en la base de datos `lavanderia.db`.
  - Pruebas integrales de dominio: instanciación de cotizaciones cambiarias, cálculo de precios de químicos en CLP, asignación de maquinaria a operarios, registro de órdenes con detalle polimórfico, validación de pago y entrega exitosa.
  - Verificación de consistencia y ejecución sin errores en consola.
