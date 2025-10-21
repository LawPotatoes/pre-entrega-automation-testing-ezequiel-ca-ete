# utils/inventory_page.py
from selenium.webdriver.common.by import By
from utils.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC

class InventoryPage(BasePage):
    """
    Page Object Model para la página de Catálogo (inventory.html).
    Contiene métodos y localizadores para la Consigna 2 y 3.
    """
    
    # --- Localizadores Comunes de UI ---
    
    HEADER_MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    SORT_CONTAINER = (By.CLASS_NAME, "product_sort_container")
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    
    # --- Localizadores de Productos ---
    
    PRODUCT_ITEM = (By.CLASS_NAME, "inventory_item")
    
    # Localizadores para el primer producto (Sauce Labs Backpack, ID 4)
    FIRST_PRODUCT_NAME_LINK = (By.ID, "item_4_title_link") 
    FIRST_PRODUCT_PRICE = (By.XPATH, "//a[@id='item_4_title_link']/ancestor::div[@class='inventory_item_label']/following-sibling::div//div[@class='inventory_item_price']")
    
    # Localizadores de botones 'Add to Cart' para la Consigna 3
    ADD_TO_CART_BACKPACK = (By.ID, "add-to-cart-sauce-labs-backpack")
    ADD_TO_CART_BIKE_LIGHT = (By.ID, "add-to-cart-sauce-labs-bike-light")
    
    def __init__(self, driver):
        super().__init__(driver)

    # ====================================================================
    # --- MÉTODOS DE LA CONSIGNAS 2: VERIFICACIÓN DE CATÁLOGO ---
    # ====================================================================

    def is_inventory_visible(self):
        """Verifica la existencia de al menos un producto, esperando que el primero sea visible."""
        try:
            # Espera explícita sobre un elemento clave del catálogo
            self.wait_for_visibility(self.FIRST_PRODUCT_NAME_LINK, timeout=5)
            return True
        except:
            return False

    def are_ui_elements_present(self):
        """Verifica la presencia de elementos importantes de la interfaz (menú y filtros)."""
        # Se asegura de que los elementos sean visibles antes de comprobar su estado.
        self.wait_for_visibility(self.HEADER_MENU_BUTTON, timeout=5)
        self.wait_for_visibility(self.SORT_CONTAINER, timeout=5)
        
        menu_present = self.find_element(self.HEADER_MENU_BUTTON).is_displayed()
        sort_present = self.find_element(self.SORT_CONTAINER).is_displayed()
        return menu_present and sort_present
        
    def get_first_product_details(self):
        """Obtiene y retorna el nombre y precio del primer producto."""
        
        # Se garantiza que el elemento está cargado antes de leer su texto
        self.wait_for_visibility(self.FIRST_PRODUCT_NAME_LINK, timeout=5) 
        
        name = self.find_element(self.FIRST_PRODUCT_NAME_LINK).text 
        price = self.find_element(self.FIRST_PRODUCT_PRICE).text
        
        return f"Nombre: {name}, Precio: {price}"

    # ====================================================================
    # --- MÉTODOS DE LA CONSIGNAS 3: INTERACCIÓN CON CARRITO ---
    # ====================================================================
        
    def add_two_items_to_cart(self):
        """Añade la Mochila y la Linterna al carrito y retorna el contador."""
        
        # 1. Añadir el primer producto
        self.find_element(self.ADD_TO_CART_BACKPACK).click()
        
        # 2. Añadir el segundo producto
        self.find_element(self.ADD_TO_CART_BIKE_LIGHT).click()
        
        # 3. Obtener el texto del contador del carrito. Se añade espera por si la actualización es lenta.
        self.wait_for_visibility(self.CART_BADGE, timeout=2)
        return self.find_element(self.CART_BADGE).text
        
    def navigate_to_cart(self):
        """Hace clic en el icono del carrito."""
        self.find_element(self.CART_ICON).click()