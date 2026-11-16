"""Página de login: https://www.saucedemo.com/"""
import logging

from selenium.webdriver.common.by import By

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    # Localizadores
    CAMPO_USUARIO = (By.ID, "user-name")
    CAMPO_CONTRASENA = (By.ID, "password")
    BOTON_LOGIN = (By.ID, "login-button")
    MENSAJE_ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    # Acciones
    def abrir(self):
        logger.info("Navegando a %s", self.URL_BASE)
        self.driver.get(self.URL_BASE)
        return self

    def iniciar_sesion(self, usuario, contrasena):
        logger.info("Iniciando sesión con el usuario '%s'", usuario)
        self.escribir(self.CAMPO_USUARIO, usuario)
        self.escribir(self.CAMPO_CONTRASENA, contrasena)
        self.hacer_clic(self.BOTON_LOGIN)

    def obtener_mensaje_error(self):
        return self.obtener_texto(self.MENSAJE_ERROR)
