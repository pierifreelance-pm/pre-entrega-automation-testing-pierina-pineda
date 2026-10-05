# Pre-entrega — Automatización de pruebas en SauceDemo

Proyecto de automatización de pruebas web sobre [saucedemo.com](https://www.saucedemo.com), un sitio demo diseñado para practicar testing.

## Propósito del proyecto

Automatizar los flujos básicos de navegación del sitio con **Selenium WebDriver** y **Python**:

| # | Caso de prueba | Qué valida |
|---|----------------|------------|
| 1 | `test_01_login_exitoso` | Login con `standard_user` / `secret_sauce`, redirección a `/inventory.html` y título "Products" |
| 2 | `test_02_verificar_titulo_inventario` | Título de la ventana ("Swag Labs") y de la sección ("Products") |
| 3 | `test_03_productos_visibles` | Que haya al menos un producto, y que el primero tenga nombre y precio |
| 4 | `test_04_validar_interfaz` | Que se vean el menú, el filtro de ordenamiento y el carrito |
| 5 | `test_05_agregar_producto_al_carrito` | Al agregar un producto, el botón cambia a "Remove" y el contador del carrito muestra 1 |
| 6 | `test_06_producto_aparece_en_el_carrito` | Al entrar al carrito, la URL es `/cart.html` y el producto agregado aparece en la lista |

Cada test abre su propio navegador y lo cierra al terminar, así **los tests son independientes**: si uno falla, no afecta a los demás.

## Tecnologías utilizadas

- **Python 3**: lenguaje principal
- **Pytest**: estructura y ejecución de los tests
- **Selenium WebDriver**: automatización del navegador (Google Chrome)
- **pytest-html**: generación del reporte HTML
- **Git y GitHub**: control de versiones

## Estructura del proyecto

```
pre-entrega-automation-testing-pierina-pineda/
├── tests/
│   └── test_saucedemo.py   # Casos de prueba (login, catálogo, carrito)
├── utils/
│   ├── __init__.py         # Marca la carpeta como paquete de Python
│   ├── helpers.py          # Funciones auxiliares: abrir Chrome, esperas, login
│   └── locators.py         # Localizadores de los elementos de la página
├── datos/
│   └── usuarios.json       # Datos de prueba (credenciales)
├── reports/
│   ├── reporte.html        # Reporte HTML generado por Pytest
│   ├── ejecucion.log       # Logs de la ejecución
│   └── capturas/           # Capturas automáticas de los tests fallidos
├── conftest.py             # Fixtures de Pytest y captura automática en fallos
├── pytest.ini              # Configuración de Pytest (carpeta de tests y logs)
├── requirements.txt        # Dependencias del proyecto
└── README.md
```

## Instalación de dependencias

Requisitos: tener instalados **Python 3** y **Google Chrome**. Selenium descarga automáticamente el driver de Chrome.

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/<tu-usuario>/pre-entrega-automation-testing-pierina-pineda.git
   cd pre-entrega-automation-testing-pierina-pineda
   ```
2. Crear y activar un entorno virtual:
   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # Mac / Linux
   ```
3. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución de las pruebas

Ejecutar todos los tests y generar el reporte HTML:

```bash
pytest -v --html=reports/reporte.html --self-contained-html
```

Otras opciones:

```bash
pytest tests/test_saucedemo.py -v                      # solo este archivo
pytest -v -k carrito                                    # solo los tests cuyo nombre contiene "carrito"
```

Para correr sin abrir la ventana del navegador (modo headless), definir la variable `HEADLESS=1`:

```bash
set HEADLESS=1 && pytest -v       # Windows (cmd)
HEADLESS=1 pytest -v              # Mac / Linux / Git Bash
```

## Reportes y evidencias

- **`reports/reporte.html`**: resultado de cada test. Se abre con cualquier navegador.
- **`reports/ejecucion.log`**: log con cada paso de la ejecución.
- **`reports/capturas/`**: si un test falla, se guarda una captura de pantalla automáticamente y también se adjunta en el reporte HTML.
