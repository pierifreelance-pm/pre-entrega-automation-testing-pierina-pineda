"""
Funciones auxiliares reutilizables por los tests.

Acá vive todo lo que NO es una validación en sí misma:
abrir el navegador, leer los datos de prueba, esperar elementos y hacer login.
Así los tests quedan cortos y fáciles de leer.
"""
import json
import logging
import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.locators import BOTON_LOGIN, CAMPO_CONTRASENA, CAMPO_USUARIO

logger = logging.getLogger(__name__)

URL_BASE = "https://www.saucedemo.com/"
TIEMPO_ESPERA = 10  # segundos máximos que esperamos a un elemento
RUTA_USUARIOS = Path(__file__).resolve().parent.parent / "datos" / "usuarios.json"


def crear_driver():
    """Abre una ventana nueva de Google Chrome lista para automatizar."""
    opciones = Options()
    opciones.add_argument("--start-maximized")
    # Desactiva el gestor de contraseñas de Chrome: su aviso de
    # "contraseña filtrada" puede tapar la página después del login.
    opciones.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })
    # Con HEADLESS=1 los tests corren sin abrir la ventana del navegador.
    if os.getenv("HEADLESS") == "1":
        opciones.add_argument("--headless=new")
        opciones.add_argument("--window-size=1920,1080")

    logger.info("Abriendo Google Chrome")
    return webdriver.Chrome(options=opciones)


def cargar_usuario(clave="usuario_valido"):
    """Lee las credenciales de prueba desde datos/usuarios.json."""
    with open(RUTA_USUARIOS, encoding="utf-8") as archivo:
        return json.load(archivo)[clave]


def esperar_visible(driver, localizador, tiempo=TIEMPO_ESPERA):
    """Espera explícita: devuelve el elemento cuando aparece en pantalla."""
    return WebDriverWait(driver, tiempo).until(
        EC.visibility_of_element_located(localizador)
    )


def esperar_url(driver, fragmento, tiempo=TIEMPO_ESPERA):
    """Espera explícita: espera a que la URL actual contenga el fragmento."""
    WebDriverWait(driver, tiempo).until(EC.url_contains(fragmento))


def esperar_texto(driver, localizador, texto, tiempo=TIEMPO_ESPERA):
    """Espera explícita: espera a que el elemento muestre el texto indicado."""
    return WebDriverWait(driver, tiempo).until(
        EC.text_to_be_present_in_element(localizador, texto)
    )


def login(driver, usuario, contrasena):
    """Entra a saucedemo.com y se loguea con las credenciales recibidas."""
    logger.info("Navegando a %s", URL_BASE)
    driver.get(URL_BASE)

    logger.info("Ingresando credenciales del usuario '%s'", usuario)
    esperar_visible(driver, CAMPO_USUARIO).send_keys(usuario)
    driver.find_element(*CAMPO_CONTRASENA).send_keys(contrasena)
    driver.find_element(*BOTON_LOGIN).click()

    esperar_url(driver, "/inventory.html")
    logger.info("Login completado, URL actual: %s", driver.current_url)
