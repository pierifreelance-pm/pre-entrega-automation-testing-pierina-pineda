"""Tests de la página de login."""
from pages.inventario_page import InventarioPage
from pages.login_page import LoginPage
from utils.helpers import cargar_usuario


def test_login_exitoso(driver):
    usuario = cargar_usuario()

    LoginPage(driver).abrir().iniciar_sesion(usuario["username"], usuario["password"])
    inventario = InventarioPage(driver).esperar_carga()

    assert "/inventory.html" in inventario.url_actual(), "ERROR: No se redirigió a /inventory.html"
    titulo = inventario.obtener_titulo()
    assert titulo == "Products", f'ERROR: Título esperado "Products", obtenido "{titulo}"'
