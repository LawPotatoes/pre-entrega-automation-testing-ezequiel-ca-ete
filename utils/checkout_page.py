# utils/checkout_page.py

from selenium.webdriver.common.by import By
from utils.base_page import BasePage
import logging

class CheckoutPage(BasePage):
    """
    Page Object para las páginas de Checkout (Your Information, Overview, Complete).
    Hereda de BasePage para usar métodos comunes de Selenium.
    """
    
    # --- Checkout Step One (Your Information) Locators ---
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    
    # --- Checkout Step Two (Overview) Locators ---
    FINISH_BUTTON = (By.ID, "finish")
    
    # --- Checkout Complete Locators ---
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".complete-header") 
    
    # --- Métodos ---
    
    def enter_user_info(self, first_name, last_name, postal_code):
        """
        Ingresa la información del usuario en el primer paso del checkout.
        """
        logging.info("Ingresando información de checkout.")
        self.find_element(self.FIRST_NAME_INPUT).send_keys(first_name)
        self.find_element(self.LAST_NAME_INPUT).send_keys(last_name)
        self.find_element(self.POSTAL_CODE_INPUT).send_keys(postal_code)
        self.click_element(self.CONTINUE_BUTTON)
        logging.info("Información ingresada. Navegando al Overview.")

    def finish_checkout(self):
        """
        Completa el proceso de compra haciendo clic en el botón 'Finish'.
        """
        logging.info("Navegando al paso final del checkout.")
        self.click_element(self.FINISH_BUTTON)
        logging.info("Checkout finalizado.")
        
    def get_success_message(self):
        """
        Retorna el mensaje de confirmación de compra exitosa.
        """
        # Espera a que el mensaje de éxito sea visible
        success_element = self.wait_for_visibility(self.SUCCESS_MESSAGE) 
        return success_element.text