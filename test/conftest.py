# tests/conftest.py

import pytest
import pytest_html.extras 
import os # Necesario para la manipulación de rutas en el hook
from utils.base_page import setup_driver, teardown_driver, BasePage

# ====================================================================
# --- FIXTURES OBLIGATORIAS DE SELENIUM ---
# ====================================================================

@pytest.fixture(scope="function")
def driver(request):
    """
    Fixture principal que inicializa el WebDriver antes de cada test 
    y lo cierra al finalizar.
    """
    driver = setup_driver()
    
    # FIX: Se añade la verificación 'if request.cls' para evitar el AttributeError.
    # Esto asegura que el driver solo se adjunte al objeto de la clase de prueba si existe.
    if request.cls:
        request.cls.driver = driver
        
    yield driver
    teardown_driver(driver)

@pytest.fixture(scope="function")
def login_setup(driver):
    """
    Fixture que navega a la URL de Sauce Demo antes de cada test de login.
    """
    driver.get("https://www.saucedemo.com/")
    return driver

# ====================================================================
# --- HOOK PARA CAPTURA DE PANTALLA EN FALLO (OBLIGATORIO) ---
# ====================================================================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook de Pytest que intercepta el resultado de la prueba.
    Si la prueba de UI falla, se toma una captura de pantalla y se adjunta al reporte HTML.
    """
    # Ejecuta el método de reporte estándar de Pytest primero
    outcome = yield
    report = outcome.get_result()

    # 1. Chequea si la prueba falló (report.failed) y si estaba en la fase 'call' (ejecución)
    if report.when == 'call' and report.failed:
        # 2. Verifica si el test usa la fixture 'driver' (es decir, es una prueba de UI)
        if 'driver' in item.funcargs:
            try:
                # El driver es accesible a través de item.funcargs, lo que funciona 
                # para pruebas de función o de clase.
                driver = item.funcargs['driver']
                
                # Obtiene el nombre completo del test para el archivo
                test_name = item.nodeid.replace("::", "_").replace("/", "_")
                
                # Crea una instancia de BasePage para llamar al método take_screenshot
                base_page = BasePage(driver)
                # El método toma la captura y devuelve la ruta relativa
                screenshot_path = base_page.take_screenshot(test_name)
                
                # 3. Adjuntar la captura al reporte HTML
                if screenshot_path:
                    # Crea la etiqueta HTML para incrustar la imagen en el reporte
                    # Nota: El path.sep debe reemplazarse por '/' en HTML
                    html = f'<div><img src="../{screenshot_path.replace(os.path.sep, "/")}" alt="screenshot" style="width:300px; height:200px;" onclick="window.open(\'../{screenshot_path.replace(os.path.sep, "/")}\')"/></div>'
                    report.extra = [pytest_html.extras.html(html)]

            except Exception as e:
                # Si falla la toma de captura, lo imprime pero no detiene la ejecución
                print(f"\n[ERROR] Fallo al intentar tomar/adjuntar la captura de pantalla: {e}")