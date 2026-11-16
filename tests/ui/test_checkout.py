"""Test del flujo completo de compra: inventario -> carrito -> checkout -> confirmación."""
from pages.carrito_page import CarritoPage
from pages.checkout_page import CheckoutPage


def test_checkout_completo(inventario):
    inventario.agregar_primer_producto_al_carrito()
    inventario.ir_al_carrito()

    carrito = CarritoPage(inventario.driver).esperar_carga()
    carrito.ir_al_checkout()

    checkout = CheckoutPage(inventario.driver)
    checkout.completar_datos("Pierina", "Pineda", "1425")
    checkout.finalizar_compra()

    mensaje = checkout.obtener_mensaje_confirmacion()
    assert mensaje == "Thank you for your order!", (
        f'ERROR: Mensaje de confirmación inesperado: "{mensaje}"'
    )
