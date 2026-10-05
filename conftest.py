"""
conftest.py: Pytest lee este archivo automáticamente antes de correr los tests.

Acá definimos:
  - Fixtures: "preparaciones" que los tests piden por parámetro (por ejemplo, un navegador abierto).
  - Un hook que saca una captura de pantalla cuando un test falla.
"""
import logging
from datetime import datetime
from pathlib import Path

import pytest

from utils.helpers import cargar_usuario, crear_driver, login

logger = logging.getLogger(__name__)

CARPETA_CAPTURAS = Path(__file__).resolve().parent / "reports" / "capturas"


@pytest.fixture
def driver():
    """Abre un navegador nuevo para cada test y lo cierra al terminar.

    Como cada test tiene su propio navegador, los tests son independientes:
    si uno falla, no afecta a los demás.
    """
    navegador = crear_driver()
    yield navegador  # acá se ejecuta el test
    logger.info("Cerrando el navegador")
    navegador.quit()


@pytest.fixture
def driver_logueado(driver):
    """Navegador que ya pasó por el login (para los tests de catálogo y carrito)."""
    usuario = cargar_usuario()
    login(driver, usuario["username"], usuario["password"])
    return driver


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Si un test falla, guarda una captura en reports/capturas/ y la adjunta al reporte HTML."""
    resultado = yield
    reporte = resultado.get_result()

    if reporte.when != "call" or not reporte.failed:
        return

    navegador = item.funcargs.get("driver")
    if navegador is None:
        return

    CARPETA_CAPTURAS.mkdir(parents=True, exist_ok=True)
    marca_tiempo = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta_captura = CARPETA_CAPTURAS / f"{item.name}_{marca_tiempo}.png"
    navegador.save_screenshot(str(ruta_captura))
    logger.error("Test fallido. Captura guardada en %s", ruta_captura)

    plugin_html = item.config.pluginmanager.getplugin("html")
    if plugin_html:
        extras = getattr(reporte, "extras", [])
        extras.append(plugin_html.extras.image(navegador.get_screenshot_as_base64()))
        reporte.extras = extras
