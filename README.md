# 🚀 Proyecto Final de Automatización de Pruebas - Ezequiel Cañete

Este proyecto consiste en un **Framework de Automatización de Pruebas** integral desarrollado en Python, siguiendo el patrón Page Object Model (POM).

El framework automatiza tanto la interfaz de usuario (UI) como los servicios de una API, demostrando una cobertura completa del flujo de negocio.

## [cite_start]🎯 Propósito del Proyecto [cite: 73]

El objetivo principal de este framework es:
1.  [cite_start]**Automatizar Pruebas de UI** para validar el flujo completo de compra en el sitio **SauceDemo.com** (Login, Navegación, Añadir al Carrito y Checkout)[cite: 27, 28].
2.  [cite_start]**Automatizar Pruebas de API** para verificar el correcto funcionamiento de los endpoints críticos (GET, POST, PUT) de la API **Reqres.in**[cite: 45].
3.  [cite_start]Implementar el patrón **Page Object Model (POM)** para crear un código modular, mantenible y escalable[cite: 20].
4.  [cite_start]Generar un **Reporte HTML detallado** y sistemático con capturas de pantalla de los fallos para la trazabilidad de los resultados[cite: 52, 54].

---

## [cite_start]🛠️ Tecnologías Utilizadas [cite: 74]

| Tecnología | Rol |
| :--- | :--- |
| **Python 3.x** | [cite_start]Lenguaje de programación principal [cite: 11] |
| **Pytest** | [cite_start]Framework de testing para la gestión y ejecución de pruebas [cite: 12] |
| **Selenium WebDriver** | [cite_start]Automatización de la interfaz de usuario (Pruebas UI) [cite: 13] |
| **Requests** | [cite_start]Biblioteca para realizar peticiones HTTP (Pruebas API) [cite: 14] |
| **Page Object Model** | [cite_start]Patrón de diseño para la organización y mantenimiento del código UI [cite: 20] |
| **Pytest-HTML** | [cite_start]Generación de reportes visuales detallados [cite: 51, 52] |
| **Git & GitHub** | [cite_start]Control de versiones y repositorio de código [cite: 15, 16] |

---

## [cite_start]📁 Estructura del Proyecto [cite: 76]

El proyecto sigue una estructura modular para separar la lógica de negocio, las pruebas y los datos:

---

## ⚙️ Instalación de Dependencias

Para ejecutar este proyecto, necesitas tener **Python 3.x** y **Git** instalados en tu sistema.

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/LawPotatoes/pre-entrega-automation-testing-ezequiel-ca-ete](https://github.com/LawPotatoes/pre-entrega-automation-testing-ezequiel-ca-ete)
    cd pre-entrega-automation-testing-ezequiel-cañete
    ```
    *(Nota: Reemplaza la URL del repositorio si es necesario)*

2.  **Instalar las bibliotecas requeridas:**
    Este comando instalará Pytest, Selenium, Requests y todas las demás dependencias listadas en el archivo `requirements.txt`[cite: 77].
    ```bash
    pip install -r requirements.txt
    ```

---

## ▶️ Ejecución de las Pruebas

El framework se ejecuta utilizando el comando de `pytest`, que automáticamente genera el reporte HTML en la carpeta `reports/`[cite: 78].

### Ejecutar todas las pruebas (UI y API)

Utiliza este comando para ejecutar todas las pruebas y generar el reporte final:

```bash
pytest -v --html=reports/reporte.html --self-contained-html


