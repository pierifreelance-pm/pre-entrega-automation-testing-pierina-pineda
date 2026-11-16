"""Páginas del checkout: datos del comprador, resumen y confirmación."""
import logging

from selenium.webdriver.common.by import By

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class CheckoutPage(BasePage):
    # Localizadores
    CAMPO_NOMBRE = (By.ID, "first-name")
    CAMPO_APELLIDO = (By.ID, "last-name")
    CAMPO_CODIGO_POSTAL = (By.ID, "postal-code")
    BOTON_CONTINUAR = (By.ID, "continue")
    BOTON_FINALIZAR = (By.ID, "finish")
    MENSAJE_CONFIRMACION = (By.CLASS_NAME, "complete-header")

    # Acciones
    def completar_datos(self, nombre, apellido, codigo_postal):
        logger.info("Completando datos del comprador: %s %s (%s)", nombre, apellido, codigo_postal)
        self.escribir(self.CAMPO_NOMBRE, nombre)
        self.escribir(self.CAMPO_APELLIDO, apellido)
        self.escribir(self.CAMPO_CODIGO_POSTAL, codigo_postal)
        self.hacer_clic(self.BOTON_CONTINUAR)

    def finalizar_compra(self):
        self.esperar_url("/checkout-step-two.html")
        self.hacer_clic(self.BOTON_FINALIZAR)
        self.esperar_url("/checkout-complete.html")
        logger.info("Compra finalizada")

    def obtener_mensaje_confirmacion(self):
        return self.obtener_texto(self.MENSAJE_CONFIRMACION)
