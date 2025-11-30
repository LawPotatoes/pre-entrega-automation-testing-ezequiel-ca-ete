# utils/base_page.py

import os
import csv
import time
import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ====================================================================
# --- FUNCIONES AUXILIARES DE DRIVER (Setup/Teardown) ---
# ====================================================================

def setup_driver():
    """
    Inicializa y configura el WebDriver de Chrome utilizando WebDriver Manager
    para asegurar la compatibilidad con el navegador instalado.
    """
    try:
        # Configuración de opciones (ej. maximizar, ignorar errores)
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--ignore-certificate-errors')
        
        # 1. Instalar y obtener el servicio del driver (si es necesario)
        service = ChromeService(ChromeDriverManager().install())
        
        # 2. Inicializar el WebDriver
        driver = webdriver.Chrome(service=service, options=options)
        
        # Configuración de espera implícita global
        driver.implicitly_wait(10)
        
        logging.info("WebDriver de Chrome inicializado correctamente.")
        return driver
        
    except WebDriverException as e:
        # Esto captura errores comunes como la falta de conexión o problemas con la versión del driver
        logging.critical(f"No se pudo inicializar el WebDriver: {e}")
        # Se asegura de que el test falle correctamente si no hay driver
        return None 
    except Exception as e:
        # Captura cualquier otro error inesperado
        logging.critical(f"Ocurrió un error inesperado durante el setup del driver: {e}")
        return None


def teardown_driver(driver):
    """Cierra el navegador y finaliza la sesión del WebDriver."""
    if driver:
        driver.quit()
        logging.info("WebDriver cerrado.")


# ====================================================================
# --- FUNCIÓN AUXILIAR PARA LECTURA DE DATOS (CSV) ---
# ====================================================================

def get_csv_data(csv_file_name):
    """
    Lee datos desde un archivo CSV.
    Retorna una lista de tuplas donde cada tupla es una fila de datos.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Construye la ruta al archivo CSV: utils/../data/users.csv
    absolute_path = os.path.join(base_dir, '..', csv_file_name)
    
    test_data = []
    try:
        with open(absolute_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la fila de encabezados
            for row in reader:
                test_data.append(tuple(row))
        logging.info(f"Datos cargados exitosamente desde {csv_file_name}. Total de filas: {len(test_data)}")
    except FileNotFoundError:
        logging.error(f"Archivo no encontrado en: {absolute_path}")
        # Devuelve una lista vacía para que la parametrización falle limpiamente
        test_data.append(('', '', 'Error', 'Data_File_Missing')) 
    except Exception as e:
        logging.error(f"Error al leer el archivo CSV: {e}")
        test_data.append(('', '', 'Error', 'CSV_Read_Error'))
        
    return test_data


# ====================================================================
# --- CLASE BASE PARA PAGE OBJECTS ---
# ====================================================================

class BasePage:
    """
    Clase base que provee métodos comunes y utilidades para todos
    los Page Objects.
    """
    
    def __init__(self, driver):
        self.driver = driver
        # Tiempo de espera explícita por defecto
        self.wait = WebDriverWait(driver, 15) 
        
    # --- Métodos de Espera y Búsqueda ---
        
    def find_element(self, by_locator):
        """Busca y retorna un elemento esperando a que esté presente."""
        try:
            return self.wait.until(EC.presence_of_element_located(by_locator))
        except TimeoutException:
            logging.error(f"Tiempo de espera agotado buscando el elemento: {by_locator}")
            raise
        
    def wait_for_visibility(self, by_locator):
        """Espera a que un elemento esté visible antes de retornarlo."""
        try:
            return self.wait.until(EC.visibility_of_element_located(by_locator))
        except TimeoutException:
            logging.error(f"Tiempo de espera agotado esperando visibilidad del elemento: {by_locator}")
            raise

    def click_element(self, by_locator):
        """Espera a que un elemento sea clickeable y luego hace clic."""
        try:
            element = self.wait.until(EC.element_to_be_clickable(by_locator))
            element.click()
        except TimeoutException:
            logging.error(f"Tiempo de espera agotado esperando que el elemento sea clickeable: {by_locator}")
            raise
    
    # --- Método de Captura de Pantalla (Requisito de Reporte) ---

    def take_screenshot(self, test_name):
        """
        Toma una captura de pantalla y la guarda en la carpeta reports/.
        Retorna la ruta relativa del archivo guardado.
        """
        if not self.driver:
            logging.error("No se puede tomar captura: el driver es None.")
            return None
            
        reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'reports')
        
        # Asegura que el directorio 'reports' exista
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
            
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"{test_name}_{timestamp}.png"
        screenshot_path = os.path.join(reports_dir, filename)
        
        try:
            self.driver.save_screenshot(screenshot_path)
            # Devuelve la ruta relativa para adjuntar al reporte HTML
            return os.path.join('reports', filename) 
        except Exception as e:
            logging.error(f"Fallo al tomar captura de pantalla para {test_name}: {e}")
            return None