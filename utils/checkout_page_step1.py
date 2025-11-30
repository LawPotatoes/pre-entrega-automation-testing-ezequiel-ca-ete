# utils/checkout_page_step1.py
from selenium.webdriver.common.by import By
from utils.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC

class CheckoutPageStep1(BasePage):
    """
    Page Object Model para la primera etapa del Checkout (Datos Personales).
    """
    
    # --- Localizadores ---
    
    HEADER_TITLE = (By.CLASS_NAME, "title")
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    ZIP_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    
    # --- Constructor ---
    
    def __init__(self, driver):
        super().__init__(driver)
        
    # --- Métodos de Acción ---
    
    def wait_for_checkout_page(self):
        """Espera a que el título de la página sea visible y lo retorna."""
        self.wait_for_visibility(self.HEADER_TITLE)
        return self.find_element(self.HEADER_TITLE).text
        
    def fill_and_continue(self, first_name, last_name, zip_code):
        """Completa los campos de información personal y hace clic en Continuar."""
        self.find_element(self.FIRST_NAME_INPUT).send_keys(first_name)
        self.find_element(self.LAST_NAME_INPUT).send_keys(last_name)
        self.find_element(self.ZIP_CODE_INPUT).send_keys(zip_code)
        
        self.find_element(self.CONTINUE_BUTTON).click()