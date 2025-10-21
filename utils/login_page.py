from selenium.webdriver.common.by import By
from utils.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage(BasePage):
    # Localizadores
    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    
    # Elemento en la página de inventario que debe aparecer (para validación)
    INVENTORY_TITLE = (By.CLASS_NAME, "title")

    def __init__(self, driver):
        super().__init__(driver) # Inicializa BasePage
        
    def login(self, username, password):
        """Realiza la acción de login."""
        self.find_element(self.USERNAME_FIELD).send_keys(username)
        self.find_element(self.PASSWORD_FIELD).send_keys(password)
        self.find_element(self.LOGIN_BUTTON).click()

    def wait_for_inventory_page(self):
        """Espera explícita obligatoria y valida el título de la página."""
        
        # 1. Espera explícita para el cambio de URL (validación de redirección)
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/inventory.html")
        )
        
        # 2. Espera explícita para la visibilidad del título 'Products'
        inventory_title_element = self.wait_for_visibility(self.INVENTORY_TITLE)
        
        return inventory_title_element.text