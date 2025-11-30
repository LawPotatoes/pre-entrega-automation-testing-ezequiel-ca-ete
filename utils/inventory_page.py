# utils/inventory_page.py

from selenium.webdriver.common.by import By
from utils.base_page import BasePage
import logging

class InventoryPage(BasePage):
    """
    Page Object para la página de Catálogo/Inventario después del login.
    Hereda de BasePage para usar métodos comunes de Selenium.
    """
    
    # --- LOCATORS ---
    
    # Elementos de validación de la página
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    TITLE_INVENTORY = (By.CLASS_NAME, "title")
    
    # Producto 1
    # CORRECCIÓN 1: Se cambia a By.ID para mayor robustez y velocidad (resuelve TimeoutException en Test 02)
    FIRST_PRODUCT_NAME = (By.ID, "item_4_title_link") 
    FIRST_PRODUCT_PRICE = (By.XPATH, "(//div[@class='inventory_item_price'])[1]")
    
    # Botones para añadir productos específicos
    ADD_TO_CART_BACKPACK = (By.ID, "add-to-cart-sauce-labs-backpack")
    ADD_TO_CART_BIKE_LIGHT = (By.ID, "add-to-cart-sauce-labs-bike-light")
    
    # Carrito
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")

    # --- Métodos de Interacción ---

    def is_inventory_visible(self):
        """
        Verifica si la página de inventario se cargó correctamente buscando el título.
        """
        try:
            element = self.wait_for_visibility(self.TITLE_INVENTORY)
            return element.text == "Products"
        except Exception:
            logging.error("No se pudo verificar la visibilidad del inventario.")
            return False

    def get_first_product_details(self):
        """
        Obtiene el nombre y precio del primer producto listado.
        """
        logging.info("Obteniendo detalles del primer producto.")
        
        # El método find_element ya usa self.wait.until(EC.presence_of_element_located)
        name_element = self.find_element(self.FIRST_PRODUCT_NAME)
        price_element = self.find_element(self.FIRST_PRODUCT_PRICE)
        
        return {
            'nombre': name_element.text,
            'precio': price_element.text
        }

    def add_two_items_to_cart(self):
        """
        Añade la Mochila y la Linterna al carrito y retorna el contador (badge).
        """
        logging.info("Añadiendo dos productos al carrito.")

        # 1. Añadir el primer producto
        self.find_element(self.ADD_TO_CART_BACKPACK).click()

        # 2. Añadir el segundo producto
        self.find_element(self.ADD_TO_CART_BIKE_LIGHT).click()

        # 3. Obtener el texto del contador del carrito. 
        # CORRECCIÓN 2: Eliminación de 'timeout=2' para evitar el TypeError
        self.wait_for_visibility(self.CART_BADGE)
        
        badge_element = self.find_element(self.CART_BADGE)
        return badge_element.text
        
    def go_to_cart(self):
        """
        Navega a la página del carrito de compras.
        """
        logging.info("Navegando al carrito de compras.")
        self.click_element(self.CART_ICON)