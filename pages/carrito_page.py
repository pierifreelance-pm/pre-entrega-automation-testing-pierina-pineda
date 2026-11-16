"""Página del carrito: /cart.html"""
import logging

from selenium.webdriver.common.by import By

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class CarritoPage(BasePage):
    # Localizadores
    PRODUCTOS_EN_CARRITO = (By.CLASS_NAME, "cart_item")
    NOMBRE_PRODUCTO = (By.CLASS_NAME, "inventory_item_name")
    BOTON_CHECKOUT = (By.ID, "checkout")

    # Acciones
    def esperar_carga(self):
        self.esperar_url("/cart.html")
        logger.info("Página del carrito cargada")
        return self

    def obtener_nombres_productos(self):
        self.esperar_visible(self.PRODUCTOS_EN_CARRITO)
        nombres = [elemento.text for elemento in self.driver.find_elements(*self.NOMBRE_PRODUCTO)]
        logger.info("Productos en el carrito: %s", nombres)
        return nombres

    def ir_al_checkout(self):
        self.hacer_clic(self.BOTON_CHECKOUT)
