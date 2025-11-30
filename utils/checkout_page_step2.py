# utils/checkout_page_step2.py
from selenium.webdriver.common.by import By
from utils.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC

class CheckoutPageStep2(BasePage):
    """
    Page Object Model para la segunda etapa del Checkout (Resumen y Confirmación).
    """
    
    # --- Localizadores ---
    
    HEADER_TITLE = (By.CLASS_NAME, "title")
    FINISH_BUTTON = (By.ID, "finish")
    TOTAL_PRICE = (By.CLASS_NAME, "summary_total_label")
    ORDER_COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    
    # --- Constructor ---
    
    def __init__(self, driver):
        super().__init__(driver)
        
    # --- Métodos de Acción y Validación ---
    
    def wait_for_overview_page(self):
        """Espera a que el título de la página de resumen sea visible y lo retorna."""
        self.wait_for_visibility(self.HEADER_TITLE)
        return self.find_element(self.HEADER_TITLE).text

    def get_total_price(self):
        """Obtiene el precio total del pedido."""
        return self.find_element(self.TOTAL_PRICE).text

    def finish_order(self):
        """Hace clic en el botón FINISH para completar la compra."""
        self.find_element(self.FINISH_BUTTON).click()
        
    def get_confirmation_message(self):
        """Obtiene el mensaje de confirmación final."""
        self.wait_for_visibility(self.ORDER_COMPLETE_HEADER)
        return self.find_element(self.ORDER_COMPLETE_HEADER).text