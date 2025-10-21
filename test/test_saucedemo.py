# tests/test_saucedemo.py
import pytest
from utils.base_page import setup_driver, teardown_driver
from utils.login_page import LoginPage 
from utils.inventory_page import InventoryPage
from utils.cart_page import CartPage

# --- Pytest Fixtures ---

@pytest.fixture(scope="module")
def driver():
    """
    Fixture principal que inicializa el WebDriver (con ChromeDriverManager)
    antes de todas las pruebas y lo cierra al finalizar el módulo.
    """
    web_driver = setup_driver()
    yield web_driver
    teardown_driver(web_driver)

@pytest.fixture
def login_setup(driver):
    """
    Fixture que asegura que cada prueba comienza en la URL de login.
    """
    driver.get("https://www.saucedemo.com/")
    yield driver

# ====================================================================
# --- CASOS DE PRUEBA OBLIGATORIOS ---
# ====================================================================

def test_01_login_exitoso(login_setup):
    """
    CONSIGNA 1: Automatizar Login con credenciales válidas y validar la redirección.
    """
    driver = login_setup

    # Acción de Login
    login_page = LoginPage(driver)
    login_page.login("standard_user", "secret_sauce") 
    
    # Validación (Espera implícita y explícita ya incluidas en wait_for_inventory_page)
    page_title = login_page.wait_for_inventory_page()

    assert "inventory.html" in driver.current_url, "ERROR: La URL no contiene 'inventory.html'."
    assert page_title == "Products", "ERROR: El título de la página no es 'Products'."

def test_02_verificacion_catalogo(driver, login_setup):
    """
    CONSIGNA 2: Verificar catálogo, elementos UI y listar el nombre/precio del primer producto.
    """
    driver = login_setup
    
    # Preparación: Login
    login_page = LoginPage(driver)
    login_page.login("standard_user", "secret_sauce")
    login_page.wait_for_inventory_page() 

    inventory_page = InventoryPage(driver)

    # 1. Validar existencia de productos (incluye espera)
    productos_visibles = inventory_page.is_inventory_visible()
    assert productos_visibles, "ERROR: No se encontraron productos en el catálogo."
    
    # 2. Validar presencia de elementos UI (menú y filtros)
    ui_elements_ok = inventory_page.are_ui_elements_present()
    assert ui_elements_ok, "ERROR: Faltan elementos importantes de la interfaz (menú o filtros)."
    
    # 3. Listar el nombre/precio del primer producto (requisito de consigna)
    detalles_producto = inventory_page.get_first_product_details()
    print(f"\n[INFO] Detalles del Primer Producto: {detalles_producto}")
    
    assert "$" in detalles_producto, "ERROR: El precio del producto no contiene el símbolo de dólar ($)."

def test_03_agregar_y_verificar_carrito(driver, login_setup):
    """
    CONSIGNA 3: Añadir dos productos, verificar el contador y el contenido del carrito.
    """
    driver = login_setup
    
    # Preparación: Login
    login_page = LoginPage(driver)
    login_page.login("standard_user", "secret_sauce")
    login_page.wait_for_inventory_page() 

    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)
    
    # 1. Añadir dos items y verificar el contador
    cart_count = inventory_page.add_two_items_to_cart()
    assert cart_count == "2", f"ERROR: El contador del carrito no es 2. Es {cart_count}."
    
    # 2. Navegar al carrito
    inventory_page.navigate_to_cart()
    cart_title = cart_page.wait_for_cart_page()
    
    assert cart_title == "Your Cart", f"ERROR: El título de la página es incorrecto: {cart_title}."
    
    # 3. Validar cantidad y nombres de productos en el carrito
    item_count = cart_page.check_product_quantities()
    assert item_count == 2, f"ERROR: Se esperaban 2 productos en el carrito, se encontraron {item_count}."
    
    item_names = cart_page.get_item_names_in_cart()
    assert cart_page.BACKPACK_NAME in item_names, f"ERROR: Falta el producto {cart_page.BACKPACK_NAME} en el carrito."
    assert cart_page.BIKE_LIGHT_NAME in item_names, f"ERROR: Falta el producto {cart_page.BIKE_LIGHT_NAME} en el carrito."
    
    print("\n[INFO] Carrito verificado exitosamente con 2 productos.")