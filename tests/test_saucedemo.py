"""
Casos de prueba de la pre-entrega sobre https://www.saucedemo.com

Cada test recibe un navegador nuevo mediante una fixture (ver conftest.py):
  - driver -navegador recién abierto, sin login
  - driver_logueado - navegador que ya hizo login con standard_user

Por eso los tests son independientes: se pueden correr solos o en cualquier
orden, y si uno falla no arrastra a los demás.
"""
import logging

from selenium.common.exceptions import TimeoutException

from utils.helpers import (
    cargar_usuario,
    esperar_texto,
    esperar_url,
    esperar_visible,
    login,
)
from utils.locators import (
    BOTON_MENU,
    BOTON_PRIMER_PRODUCTO,
    CONTADOR_CARRITO,
    FILTRO_ORDENAR,
    ICONO_CARRITO,
    NOMBRE_PRODUCTO,
    PRECIO_PRODUCTO,
    PRODUCTOS,
    PRODUCTOS_EN_CARRITO,
    TITULO_PAGINA,
)

logger = logging.getLogger(__name__)


# 1. Automatización de Login
def test_01_login_exitoso(driver):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    assert "/inventory.html" in driver.current_url, "ERROR: No se redirigió a /inventory.html"
    titulo = esperar_visible(driver, TITULO_PAGINA).text
    assert titulo == "Products", f'ERROR: Título esperado "Products", obtenido "{titulo}"'


# ---------------------------------------------------------------------------
# 2. Navegación y verificación del catálogo
# ---------------------------------------------------------------------------
def test_02_verificar_titulo_inventario(driver_logueado):
    titulo_ventana = driver_logueado.title
    titulo_seccion = esperar_visible(driver_logueado, TITULO_PAGINA).text

    assert titulo_ventana == "Swag Labs", (
        f'ERROR: Título de ventana esperado "Swag Labs", obtenido "{titulo_ventana}"'
    )
    assert titulo_seccion == "Products", (
        f'ERROR: Título de sección esperado "Products", obtenido "{titulo_seccion}"'
    )


def test_03_productos_visibles(driver_logueado):
    esperar_visible(driver_logueado, PRODUCTOS)
    productos = driver_logueado.find_elements(*PRODUCTOS)

    assert len(productos) > 0, "ERROR: No se encontraron productos visibles"
    logger.info("Productos encontrados: %d", len(productos))

    primer_producto = productos[0]
    nombre = primer_producto.find_element(*NOMBRE_PRODUCTO).text
    precio = primer_producto.find_element(*PRECIO_PRODUCTO).text
    logger.info("Primer producto: %s - %s", nombre, precio)

    assert nombre != "", "ERROR: El primer producto no tiene nombre"
    assert precio.startswith("$"), f'ERROR: Precio con formato inválido: "{precio}"'


def test_04_validar_interfaz(driver_logueado):
    assert esperar_visible(driver_logueado, BOTON_MENU).is_displayed(), "ERROR: Menú no está visible"
    assert esperar_visible(driver_logueado, FILTRO_ORDENAR).is_displayed(), "ERROR: Filtro no está visible"
    assert esperar_visible(driver_logueado, ICONO_CARRITO).is_displayed(), "ERROR: Carrito no está visible"


# ---------------------------------------------------------------------------
# 3. Interacción con productos (carrito)
# ---------------------------------------------------------------------------
def test_05_agregar_producto_al_carrito(driver_logueado):
    esperar_visible(driver_logueado, BOTON_PRIMER_PRODUCTO).click()

    # Al hacer clic, la página reemplaza el botón por uno nuevo que dice "Remove".
    # Por eso no reutilizamos el botón viejo: esperamos a que aparezca el texto nuevo.
    try:
        esperar_texto(driver_logueado, BOTON_PRIMER_PRODUCTO, "Remove")
    except TimeoutException:
        boton = driver_logueado.find_element(*BOTON_PRIMER_PRODUCTO).text
        raise AssertionError(f'ERROR: El botón no cambió a "Remove", muestra "{boton}"')

    contador = esperar_visible(driver_logueado, CONTADOR_CARRITO).text
    assert contador == "1", f"ERROR: Se esperaba 1 en el carrito, obtuvo {contador}"


def test_06_producto_aparece_en_el_carrito(driver_logueado):
    primer_producto = esperar_visible(driver_logueado, PRODUCTOS)
    nombre_producto = primer_producto.find_element(*NOMBRE_PRODUCTO).text

    logger.info("Agregando al carrito: %s", nombre_producto)
    esperar_visible(driver_logueado, BOTON_PRIMER_PRODUCTO).click()
    esperar_visible(driver_logueado, CONTADOR_CARRITO)

    driver_logueado.find_element(*ICONO_CARRITO).click()
    esperar_url(driver_logueado, "/cart.html")
    assert "/cart.html" in driver_logueado.current_url, "ERROR: No se redirigió a /cart.html"

    esperar_visible(driver_logueado, PRODUCTOS_EN_CARRITO)
    nombres_en_carrito = [
        elemento.text for elemento in driver_logueado.find_elements(*NOMBRE_PRODUCTO)
    ]
    assert nombre_producto in nombres_en_carrito, (
        f'ERROR: "{nombre_producto}" no está en el carrito. Productos encontrados: {nombres_en_carrito}'
    )
