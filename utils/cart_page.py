# utils/cart_page.py
from selenium.webdriver.common.by import By
from utils.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CartPage(BasePage):
    # Localizadores
    CART_TITLE = (By.CLASS_NAME, "title")
    CART_ITEM_COUNT = (By.CLASS_NAME, "cart_item")
    
    # Nombres de los productos que esperamos encontrar
    BACKPACK_NAME = "Sauce Labs Backpack"
    BIKE_LIGHT_NAME = "Sauce Labs Bike Light"

    def __init__(self, driver):
        super().__init__(driver)
        
    def wait_for_cart_page(self):
        """Espera a que la página del carrito cargue y valida el título."""
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/cart.html")
        )
        return self.find_element(self.CART_TITLE).text
        
    def get_item_names_in_cart(self):
        """Devuelve una lista de los nombres de los productos en el carrito."""
        # Se asume que los elementos están visibles después de wait_for_cart_page()
        
        # Encuentra todos los nombres de los productos
        name_elements = self.driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        
        # Retorna el texto de cada elemento en una lista
        return [elem.text for elem in name_elements]

    def check_product_quantities(self):
        """Cuenta cuántos items diferentes están en el carrito."""
        items = self.driver.find_elements(*self.CART_ITEM_COUNT)
        return len(items)