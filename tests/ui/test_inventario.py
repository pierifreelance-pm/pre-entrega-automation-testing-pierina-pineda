"""Tests de la página de inventario (catálogo).

La fixture "inventario" (ver conftest.py) ya hizo el login y
devuelve la página de inventario lista para usar.
"""


def test_titulo_inventario(inventario):
    titulo_ventana = inventario.driver.title
    titulo_seccion = inventario.obtener_titulo()

    assert titulo_ventana == "Swag Labs", (
        f'ERROR: Título de ventana esperado "Swag Labs", obtenido "{titulo_ventana}"'
    )
    assert titulo_seccion == "Products", (
        f'ERROR: Título de sección esperado "Products", obtenido "{titulo_seccion}"'
    )


def test_productos_visibles(inventario):
    productos = inventario.obtener_productos()
    assert len(productos) > 0, "ERROR: No se encontraron productos visibles"

    nombre, precio = inventario.obtener_nombre_y_precio_primer_producto()
    assert nombre != "", "ERROR: El primer producto no tiene nombre"
    assert precio.startswith("$"), f'ERROR: Precio con formato inválido: "{precio}"'


def test_elementos_de_interfaz_visibles(inventario):
    assert inventario.esta_visible(inventario.BOTON_MENU), "ERROR: Menú no está visible"
    assert inventario.esta_visible(inventario.FILTRO_ORDENAR), "ERROR: Filtro no está visible"
    assert inventario.esta_visible(inventario.ICONO_CARRITO), "ERROR: Carrito no está visible"
