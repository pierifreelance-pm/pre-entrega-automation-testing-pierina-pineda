"""
Localizadores de los elementos de saucedemo.com.

Cada localizador es una tupla (estrategia, valor) que después se usa así:
    driver.find_element(*CAMPO_USUARIO)

Tenerlos todos juntos acá hace que, si la página cambia un id o una clase,
solo haya que corregirlo en un único lugar.
"""
from selenium.webdriver.common.by import By

# --- Página de login ---
CAMPO_USUARIO = (By.ID, "user-name")
CAMPO_CONTRASENA = (By.ID, "password")
BOTON_LOGIN = (By.ID, "login-button")

# --- Página de inventario (catálogo) ---
TITULO_PAGINA = (By.CLASS_NAME, "title")
PRODUCTOS = (By.CLASS_NAME, "inventory_item")
NOMBRE_PRODUCTO = (By.CLASS_NAME, "inventory_item_name")
PRECIO_PRODUCTO = (By.CLASS_NAME, "inventory_item_price")
BOTON_PRIMER_PRODUCTO = (By.CSS_SELECTOR, ".inventory_item button")
BOTON_MENU = (By.ID, "react-burger-menu-btn")
FILTRO_ORDENAR = (By.CLASS_NAME, "product_sort_container")

# --- Carrito ---
ICONO_CARRITO = (By.CLASS_NAME, "shopping_cart_link")
CONTADOR_CARRITO = (By.CLASS_NAME, "shopping_cart_badge")
PRODUCTOS_EN_CARRITO = (By.CLASS_NAME, "cart_item")
