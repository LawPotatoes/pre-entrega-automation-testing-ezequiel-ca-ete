# utils/login_page.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging

# Se asume que BasePage está en utils.base_page
from utils.base_page import BasePage 

class LoginPage(BasePage):
    """
    Page Object para la página de login (https://www.saucedemo.com/).
    Hereda de BasePage para usar métodos comunes de Selenium.
    """
    
    # --- LOCATORS ---
    
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    
    # Locator para el mensaje de error (usado en Test 04)
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']") 
    
    # Locator para verificar la carga de la página de inventario (usado en espera)
    INVENTORY_CONTAINER = (By.ID, "inventory_container") 

    # --- ACCIONES ---

    def login(self, username, password):
        """
        Realiza la acción de login con las credenciales proporcionadas.
        """
        logging.info(f"Intentando login con usuario: {username}")
        self.find_element(self.USERNAME_INPUT).send_keys(username)
        self.find_element(self.PASSWORD_INPUT).send_keys(password)
        self.click_element(self.LOGIN_BUTTON)
        # La verificación de éxito o fallo se deja a la capa de test.
        
    def get_error_message(self):
        """
        [CORRECCIÓN para Test 04] 
        Retorna el texto del mensaje de error que aparece tras un login fallido.
        """
        # Espera que el mensaje de error sea visible y luego obtiene su texto
        try:
            error_element = self.wait_for_visibility(self.ERROR_MESSAGE)
            logging.warning("Mensaje de error detectado.")
            return error_element.text
        except TimeoutException:
            logging.error("No se encontró el mensaje de error tras el login fallido.")
            # Si no lo encuentra, lanza una excepción para fallar el test
            raise

    def wait_for_inventory_page(self):
        """
        [CORRECCIÓN para Tests 02, 05]
        Espera explícitamente a que la página de inventario cargue después de un login exitoso.
        """
        logging.info("Esperando la carga de la página de inventario...")
        try:
            # Espera a que el contenedor principal del inventario esté presente en el DOM
            self.wait.until(EC.presence_of_element_located(self.INVENTORY_CONTAINER))
            logging.info("Página de inventario cargada.")
            return True
        except TimeoutException:
            logging.error("Tiempo de espera agotado: Fallo al cargar la página de inventario después del login.")
            return False