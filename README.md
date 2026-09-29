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

### 18 de Agosto de 2026
- **Planificación Inicial:** Definición del alcance del sistema para el negocio de Lavandería.
- **Configuración del Entorno:** Inicialización del repositorio Git y creación del archivo `.gitignore` para excluir cachés compiladas de Python (`__pycache__/`, `*.pyc`).

### 25 de Agosto de 2026
- **Módulo de Conexión (`conectar.py`):** Creación del módulo centralizado de conexión a SQLite configurando la base de datos `lavanderia.db` y habilitando la integridad referencial con `PRAGMA foreign_keys = ON`.
- **Módulo de Moneda e Insumos (`model/cotizacion_dolar.py` y `model/producto_quimico.py`):**
  - Implementación de `CotizacionDolar` con atributos privados `__fecha` y `__valor_dolar`, validación de montos positivos y método `obtenerValorDolar()`.
  - Implementación de `ProductoQuimico` con validación de nombre, precio en dólares y método `calcularPrecioPesos()` para convertir el costo de insumos a moneda nacional.

### 1 de Septiembre de 2026
- **Jerarquía de Personal (`model/empleado.py`, `model/cajero.py`, `model/operario.py`):**
  - Creación de la clase abstracta `Empleado` con encapsulamiento sobre `__id_empleado` y validación de enteros positivos.
  - Implementación de `Cajero` heredando de `Empleado`, incorporando métodos de atención comercial: `recibirPrendas()`, `registrarOrden()`, `cobrarOrden()` y `entregarPrendas()`.
  - Implementación de `Operario` heredando de `Empleado`, con gestión de máquinas asignadas y métodos `procesarPrenda()` y `operarMaquina()`.
- **Modelado de Equipamiento (`model/maquina.py`):** Creación de la clase `Maquina` con identificador único y método `iniciarLavado()`.

### 8 de Septiembre de 2026
- **Módulo de Clientes (`model/cliente.py`):** Creación de la clase `Cliente` con atributo privado `__rut`, setter con expresión regular y algoritmo completo de validación de dígito verificador para RUT chileno (`validarRut()`).
- **Abstracción de Prendas (`model/prenda.py`):** Creación de la clase abstracta base `Prenda` mediante `abc.ABC`, definiendo atributos protegidos/privados (`__estado_inicial`, `__lavado_seco`, `__producto_quimico`), validación de estado físico de la prenda y los métodos abstractos `calcularCosto()` y `calcularTiempoLavado()`.

### 15 de Septiembre de 2026
- **Polimorfismo de Prendas (`model/ropa_normal.py`, `model/alfombra.py`, `model/edredon_cobertor.py`):**
  - Creación de `RopaNormal`, `Alfombra` y `EdredonCobertor` heredando de `Prenda`.
  - Sobrescritura de `calcularCosto()` aplicando tarifas especializadas según material y tipo de tratamiento (agua o lavado en seco).
  - Sobrescritura de `calcularTiempoLavado()` retornando tiempos estimados diferenciados de ciclo.
- **Líneas de Detalle y Pedidos (`model/detalle_orden.py` y `model/orden.py`):**
  - Creación de `DetalleOrden` para cálculo automático de subtotales multiplicando costo unitario polimórfico por la cantidad ingresada.
  - Creación de `Orden` para consolidar cliente, cajero y lista de detalles, con validación de identificación, cálculo del total general, verificación de pago y control de entrega segura.

### 22 de Septiembre de 2026
- **Diseño de la Capa DAO (`dao/`):**
  - Creación del paquete `dao` con su respectivo `__init__.py`.
  - Implementación de la clase base `DAO` (`dao/dao.py`) para encapsular la conexión compartida y el cursor de SQLite.
  - Creación de DAOs para entidades independientes:
    - `ClienteDAO` (`dao/cliente_dao.py`): Creación de tabla y operaciones de persistencia para clientes.
    - `EmpleadoDAO` (`dao/empleado_dao.py`): Creación de tabla base de empleados.
    - `MaquinaDAO` (`dao/maquina_dao.py`): Creación de tabla para equipos de lavado.
    - `ProductoQuimicoDAO` (`dao/producto_quimico_dao.py`): Tabla de insumos químicos y costos.
    - `CotizacionDolarDAO` (`dao/cotizacion_dolar_dao.py`): Tabla de registro histórico de cotizaciones.

### 28 de Septiembre de 2026
- **Especialización de DAOs Relacionales y con Herencia:**
  - Implementación de `CajeroDAO` (`dao/cajero_dao.py`) y `OperarioDAO` (`dao/operario_dao.py`) extendiendo de `EmpleadoDAO`.
  - Implementación de `PrendaDAO` (`dao/prenda_dao.py`) con relación foránea a `producto_quimico`.
  - Implementación de `RopaNormalDAO`, `AlfombraDAO` y `EdredonCobertorDAO` extendiendo de `PrendaDAO`.
  - Implementación de `OrdenDAO` (`dao/orden_dao.py`) y `DetalleOrdenDAO` (`dao/detalle_orden_dao.py`) con integridad referencial completa hacia clientes, cajeros y prendas.
- **Integración y Verificación del Sistema (`main.py`):**
  - Desarrollo del script principal `main.py` integrando la creación ordenada de todas las tablas relacionales en `lavanderia.db`.
  - Ejecución de pruebas integrales simulando el ciclo completo del negocio: recepción, conversión de divisas, asignación de maquinaria, procesamiento, cálculo de totales, cobro y entrega.
