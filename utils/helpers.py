"""
Funciones auxiliares reutilizables por los tests.

Acá vive lo que no pertenece a ninguna página en particular:
abrir el navegador y leer los datos de prueba.
(Las esperas y las acciones sobre la página están en la carpeta pages/).
"""
import json
import logging
import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

logger = logging.getLogger(__name__)

CARPETA_DATOS = Path(__file__).resolve().parent.parent / "datos"


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
    with open(CARPETA_DATOS / "usuarios.json", encoding="utf-8") as archivo:
        return json.load(archivo)[clave]
