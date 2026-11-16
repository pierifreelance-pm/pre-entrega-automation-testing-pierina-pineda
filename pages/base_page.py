"""
BasePage: clase "madre" de todas las páginas.

Tiene las acciones genéricas que se repiten en cualquier página
(esperar, hacer clic, escribir, leer texto). Las demás páginas
heredan de esta clase y así no repiten ese código.
"""
import logging

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)


class BasePage:
    URL_BASE = "https://www.saucedemo.com/"
    TIEMPO_ESPERA = 10  # segundos máximos que esperamos a un elemento

    def __init__(self, driver):
        self.driver = driver
        self.espera = WebDriverWait(driver, self.TIEMPO_ESPERA)

    def esperar_visible(self, localizador):
        """Espera explícita: devuelve el elemento cuando aparece en pantalla."""
        return self.espera.until(EC.visibility_of_element_located(localizador))

    def esperar_url(self, fragmento):
        """Espera explícita: espera a que la URL contenga el fragmento indicado."""
        self.espera.until(EC.url_contains(fragmento))

    def esperar_texto(self, localizador, texto):
        """Espera explícita: espera a que el elemento muestre el texto indicado."""
        self.espera.until(EC.text_to_be_present_in_element(localizador, texto))

    def hacer_clic(self, localizador):
        self.espera.until(EC.element_to_be_clickable(localizador)).click()

    def escribir(self, localizador, texto):
        campo = self.esperar_visible(localizador)
        campo.clear()
        campo.send_keys(texto)

    def obtener_texto(self, localizador):
        return self.esperar_visible(localizador).text

    def esta_visible(self, localizador):
        """Devuelve True si el elemento aparece en pantalla, False si no aparece."""
        try:
            self.esperar_visible(localizador)
            return True
        except TimeoutException:
            return False

    def url_actual(self):
        return self.driver.current_url
