# utils/cart_page.py

from selenium.webdriver.common.by import By
from utils.base_page import BasePage

class CartPage(BasePage):
    """
    Page Object Model para la página del Carrito de Compras.
    """
    
    # --- Localizadores ---
    
    CART_URL = "cart.html"
    HEADER_TITLE = (By.CLASS_NAME, "title")
    CART_ITEM_LIST = (By.CLASS_NAME, "cart_list")
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BUTTON = (By.ID, "checkout") # <-- ¡El localizador clave!
    
    # --- Constructor ---
    
    def __init__(self, driver):
        super().__init__(driver)
        
    # --- Métodos de Validación y Acción ---
    
    def wait_for_cart_page(self):
        """Espera a que el carrito esté visible y verifica que la URL es correcta."""
        self.wait_for_visibility(self.HEADER_TITLE)
        assert self.CART_URL in self.driver.current_url, "No se cargó la página del carrito."
        
    def get_cart_item_count(self):
        """Cuenta la cantidad de ítems presentes en el carrito."""
        # Se asume que get_cart_item_count regresa una lista de elementos
        return len(self.driver.find_elements(*self.CART_ITEM))
        
    def get_item_names(self):
        """Retorna una lista con los nombres de los ítems en el carrito."""
        item_names = []
        # Encuentra todos los elementos del carrito
        items = self.driver.find_elements(*self.CART_ITEM)
        for item in items:
            # Dentro de cada ítem, busca el nombre del producto
            name_element = item.find_element(By.CLASS_NAME, "inventory_item_name")
            item_names.append(name_element.text)
        return item_names

    # --- MÉTODO AGREGADO PARA EL PROYECTO FINAL ---
    def click_checkout(self):
        """
        Hace clic en el botón 'Checkout' para iniciar el proceso de compra.
        """
        self.find_element(self.CHECKOUT_BUTTON).click()