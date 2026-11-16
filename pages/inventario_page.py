"""Página de inventario (catálogo de productos): /inventory.html"""
import logging

from selenium.webdriver.common.by import By

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class InventarioPage(BasePage):
    # Localizadores
    TITULO = (By.CLASS_NAME, "title")
    PRODUCTOS = (By.CLASS_NAME, "inventory_item")
    NOMBRE_PRODUCTO = (By.CLASS_NAME, "inventory_item_name")
    PRECIO_PRODUCTO = (By.CLASS_NAME, "inventory_item_price")
    BOTON_PRIMER_PRODUCTO = (By.CSS_SELECTOR, ".inventory_item button")
    BOTON_MENU = (By.ID, "react-burger-menu-btn")
    FILTRO_ORDENAR = (By.CLASS_NAME, "product_sort_container")
    ICONO_CARRITO = (By.CLASS_NAME, "shopping_cart_link")
    CONTADOR_CARRITO = (By.CLASS_NAME, "shopping_cart_badge")

    # Acciones
    def esperar_carga(self):
        self.esperar_url("/inventory.html")
        self.esperar_visible(self.PRODUCTOS)
        logger.info("Página de inventario cargada")
        return self

    def obtener_titulo(self):
        return self.obtener_texto(self.TITULO)

    def obtener_productos(self):
        self.esperar_visible(self.PRODUCTOS)
        return self.driver.find_elements(*self.PRODUCTOS)

    def obtener_nombre_y_precio_primer_producto(self):
        primer_producto = self.obtener_productos()[0]
        nombre = primer_producto.find_element(*self.NOMBRE_PRODUCTO).text
        precio = primer_producto.find_element(*self.PRECIO_PRODUCTO).text
        logger.info("Primer producto: %s - %s", nombre, precio)
        return nombre, precio

    def agregar_primer_producto_al_carrito(self):
        """Agrega el primer producto y devuelve su nombre."""
        nombre, _ = self.obtener_nombre_y_precio_primer_producto()
        logger.info("Agregando al carrito: %s", nombre)
        self.hacer_clic(self.BOTON_PRIMER_PRODUCTO)
        return nombre

    def esperar_boton_remove(self):
        # Al agregar el producto, la página reemplaza el botón por uno nuevo
        # que dice "Remove". Esperamos a que aparezca ese texto.
        self.esperar_texto(self.BOTON_PRIMER_PRODUCTO, "Remove")

    def obtener_cantidad_carrito(self):
        return self.obtener_texto(self.CONTADOR_CARRITO)

    def ir_al_carrito(self):
        self.hacer_clic(self.ICONO_CARRITO)
