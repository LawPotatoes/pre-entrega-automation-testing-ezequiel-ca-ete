import pytest
import logging

# Importar funciones y clases auxiliares
from utils.base_page import get_csv_data 
from utils.login_page import LoginPage
from utils.inventory_page import InventoryPage
from utils.cart_page import CartPage
from utils.checkout_page import CheckoutPage

# Usar el logger configurado en base_page
logger = logging.getLogger(__name__)

# ====================================================================
# --- TEST SUITE: SAUCE DEMO UI TESTING ---
# ====================================================================

def test_01_login_exitoso(driver, login_setup):
    """
    CONSIGNA: Validar el login con el usuario 'standard_user' y verificar la URL.
    """
    driver = login_setup
    
    logger.info("Iniciando prueba de Login Exitoso.")
    
    login_page = LoginPage(driver)
    login_page.login("standard_user", "secret_sauce")
    
    # 1. Espera explícita para asegurar que la página de inventario cargó
    assert login_page.wait_for_inventory_page(), "ERROR: La página de inventario no cargó después del login."
    
    # 2. Validación final de la URL
    assert driver.current_url == "https://www.saucedemo.com/inventory.html", "ERROR: La URL no es la esperada después del login."
    logger.info("Login Exitoso completado. URL validada.")


def test_02_verificacion_catalogo(driver, login_setup):
    """
    CONSIGNA: Verificar la presencia de elementos UI y obtener detalles del primer producto.
    """
    driver = login_setup

    # Login
    login_page = LoginPage(driver)
    login_page.login("standard_user", "secret_sauce")
    
    # CORRECCIÓN CRÍTICA: Esperar la carga del inventario antes de proceder
    login_page.wait_for_inventory_page()

    inventory_page = InventoryPage(driver)

    # 1. Validación de la página (Assert de la consigna)
    assert inventory_page.is_inventory_visible(), "ERROR: La página de inventario no está visible."
    
    # 2. Obtener detalles del primer producto
    primer_producto = inventory_page.get_first_product_details()

    assert primer_producto['nombre'] == "Sauce Labs Backpack", "ERROR: El nombre del primer producto no coincide."
    assert primer_producto['precio'] == "$29.99", "ERROR: El precio del primer producto no coincide."
    
    logger.info(f"Catálogo verificado. Primer producto: {primer_producto['nombre']} - {primer_producto['precio']}")


def test_03_agregar_y_verificar_carrito(driver, login_setup):
    """
    CONSIGNA: Añadir dos productos y verificar el badge del carrito y su contenido.
    """
    driver = login_setup

    # Login
    login_page = LoginPage(driver)
    login_page.login("standard_user", "secret_sauce")
    login_page.wait_for_inventory_page()

    inventory_page = InventoryPage(driver)

    # 1. Añadir productos y verificar badge 
    badge_count = inventory_page.add_two_items_to_cart()
    
    assert badge_count == '2', f"ERROR: El contador del carrito es incorrecto, se esperaba '2' pero se obtuvo '{badge_count}'."
    logger.info("Dos productos añadidos y contador de carrito validado.")

    # 2. Navegar al carrito y verificar contenido
    inventory_page.go_to_cart()
    cart_page = CartPage(driver)
    
    # CORRECCIÓN 1: 'get_cart_items_count' -> 'get_cart_item_count'
    items_en_carrito = cart_page.get_cart_item_count() 

    assert items_en_carrito == 2, f"ERROR: Se esperaba 2 items en el carrito, se obtuvieron {items_en_carrito}."
    logger.info("Contenido del carrito validado.")


@pytest.mark.parametrize(
    "username,password,expected_result,test_case",
    get_csv_data("data/users.csv")[1:] # Salta el primer registro, toma los de error
)
def test_04_login_fallido_y_bloqueado(login_setup, username, password, expected_result, test_case):
    """
    CONSIGNA FINAL: Test de logins fallidos (Usuario bloqueado e Inválido) usando parametrización.
    """
    driver = login_setup

    logger.info(f"Iniciando prueba de Login Fallido para caso: {test_case}")
    login_page = LoginPage(driver)
    login_page.login(username, password)

    # Esperamos que aparezca el mensaje de error 
    error_message = login_page.get_error_message()
    
    # Validación del mensaje de error
    if test_case == "Login_Bloqueado":
        assert "Epic sadface: Sorry, this user has been locked out." in error_message
    elif test_case == "Login_Fallido":
        assert "Epic sadface: Username and password do not match any user in this service" in error_message
    
    logger.info(f"Caso {test_case} validado. Mensaje de error correcto: {error_message[:40]}...")


def test_05_checkout_completo(driver, login_setup):
    """
    CONSIGNA FINAL: Automatizar el flujo completo de compra (añadir, checkout, finalizar).
    """
    driver = login_setup

    # --- 1. Preparación: Login y Añadir Productos ---
    logger.info("Iniciando flujo de Checkout completo: Login y añadir items.")
    login_page = LoginPage(driver)
    login_page.login("standard_user", "secret_sauce")

    # CORRECCIÓN CRÍTICA: Esperar la carga del inventario
    login_page.wait_for_inventory_page() 

    inventory_page = InventoryPage(driver)
    inventory_page.add_two_items_to_cart()

    # --- 2. Checkout ---
    inventory_page.go_to_cart()

    cart_page = CartPage(driver)
    # CORRECCIÓN 2: 'go_to_checkout' -> 'click_checkout'
    cart_page.click_checkout() 

    # --- 3. Información de Usuario ---
    checkout_page = CheckoutPage(driver)
    checkout_page.enter_user_info("Ezequiel", "Cañete", "1600")

    # --- 4. Validación Final ---
    checkout_page.finish_checkout()
    
    # Validar mensaje de éxito
    success_message = checkout_page.get_success_message()
    assert success_message == "Thank you for your order!", "ERROR: Mensaje de confirmación incorrecto."
    
    logger.info("Checkout completo validado exitosamente.")