# 🐍 Pre-Entrega: Automatización de E-commerce - SauceDemo

## 1. Propósito del Proyecto

El objetivo de este proyecto es aplicar los conocimientos de automatización de pruebas adquiridos, utilizando el patrón **Page Object Model (POM)**. Se automatizan flujos clave de navegación y compra en el sitio demo `www.saucedemo.com`, demostrando la capacidad de interactuar con elementos web, manejar aserciones y generar reportes de ejecución.

## 2. Tecnologías y Herramientas Utilizadas

Este proyecto fue desarrollado utilizando las siguientes tecnologías, cumpliendo con las consignas:

| Tecnología | Propósito |
| :--- | :--- |
| **Python 3.x** | Lenguaje de programación principal. |
| **Pytest** | Framework de pruebas para estructurar y ejecutar los casos de prueba. |
| **Selenium WebDriver** | Biblioteca para interactuar y automatizar el navegador. |
| **WebDriver Manager** | Para manejar automáticamente la descarga y configuración del Chrome Driver. |
| **pytest-html** | Plugin para generar reportes detallados en formato HTML. |
| **Git & GitHub** | Sistema de control de versiones y repositorio público. |

***

## 3. Estructura del Proyecto

El proyecto sigue una estructura limpia y modular basada en el patrón POM, lo que garantiza la reusabilidad y mantenibilidad del código:

***

## 4. Configuración e Instalación de Dependencias

Para ejecutar las pruebas localmente, sigue estos pasos:

1.  **Clonar el Repositorio:**
    ```bash
    git clone [https://www.youtube.com/watch?v=dnxdIzF8p3k](https://www.youtube.com/watch?v=dnxdIzF8p3k)
    cd [nombre del repositorio]
    ```

2.  **Crear un Entorno Virtual (Recomendado):**
    ```bash
    python -m venv venv
    # Activar entorno virtual (Windows)
    .\venv\Scripts\activate
    # Activar entorno virtual (macOS/Linux)
    # source venv/bin/activate 
    ```

3.  **Instalar Dependencias:**
    Instala todas las librerías necesarias (incluyendo Selenium, Pytest y `pytest-html`):
    ```bash
    pip install -r requirements.txt
    ```

***

## 5. Ejecución de las Pruebas

### Comando para Ejecutar las Pruebas

Ejecuta todas las pruebas en el archivo `test_saucedemo.py` con el siguiente comando, asegurándote de estar en la carpeta raíz del proyecto y de tener el entorno virtual activo:

```bash
pytest -v
