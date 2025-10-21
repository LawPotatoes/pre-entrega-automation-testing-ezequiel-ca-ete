# utils/base_page.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class BasePage:
    """
    Clase Base que proporciona funcionalidades comunes de Selenium
    (Navegación, búsqueda de elementos, esperas, etc.)
    """
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://www.saucedemo.com/"

    def go_to_url(self, url):
        """Navega a una URL específica."""
        self.driver.get(url)

    def find_element(self, locator):
        """Encuentra un elemento utilizando un localizador."""
        return self.driver.find_element(*locator)

    def wait_for_visibility(self, locator, timeout=10):
        """Espera explícita para que un elemento sea visible."""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

# --- Funciones de Setup y Teardown para Pytest Fixtures ---
# IMPORTANTE: Estas funciones DEBEN estar fuera de la clase BasePage.

def setup_driver():
    """Configura e inicializa el WebDriver de Chrome con WebDriver Manager."""
    # Instala o usa el driver de Chrome disponible
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(5)  # Espera implícita
    driver.maximize_window()
    return driver

def teardown_driver(driver):
    """Cierra el navegador."""
    driver.quit()