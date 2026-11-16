"""Tests del carrito de compras."""
from pages.carrito_page import CarritoPage


def test_agregar_producto_al_carrito(inventario):
    inventario.agregar_primer_producto_al_carrito()

    inventario.esperar_boton_remove()
    cantidad = inventario.obtener_cantidad_carrito()
    assert cantidad == "1", f"ERROR: Se esperaba 1 en el carrito, obtuvo {cantidad}"


def test_producto_aparece_en_el_carrito(inventario):
    nombre_producto = inventario.agregar_primer_producto_al_carrito()
    inventario.ir_al_carrito()

    carrito = CarritoPage(inventario.driver).esperar_carga()
    assert "/cart.html" in carrito.url_actual(), "ERROR: No se redirigió a /cart.html"

    nombres_en_carrito = carrito.obtener_nombres_productos()
    assert nombre_producto in nombres_en_carrito, (
        f'ERROR: "{nombre_producto}" no está en el carrito. Productos encontrados: {nombres_en_carrito}'
    )
