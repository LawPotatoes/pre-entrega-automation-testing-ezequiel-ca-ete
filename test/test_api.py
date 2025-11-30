# tests/test_api.py
import pytest
import requests
import json
import logging

# Configuración básica de logging para registrar los pasos en la consola
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# *** CAMBIO: Usamos JSONPlaceholder, una API estable para pruebas CRUD ***
BASE_URL = "https://jsonplaceholder.typicode.com" 

# ====================================================================
# --- CASOS DE PRUEBA DE API (OBLIGATORIO: Mínimo 3) ---
# ====================================================================

def test_01_get_list_resources():
    """
    CONSIGNA: Prueba GET - Verificar la obtención de un recurso por ID (Status 200).
    Endpoint: /posts/1
    """
    resource_id = 1
    endpoint = f"{BASE_URL}/posts/{resource_id}"
    
    logging.info(f"Enviando solicitud GET a: {endpoint}")
    response = requests.get(endpoint)
    
    # 1. Validar el Status Code (200 OK)
    assert response.status_code == 200, f"Error: Se esperaba Status 200, se obtuvo {response.status_code}"
    logging.info(f"Status Code 200 OK obtenido.")
    
    # 2. Validar el formato de la respuesta
    assert 'application/json' in response.headers.get('Content-Type'), "Error: El Content-Type no es JSON"
    
    # 3. Validar el contenido
    data = response.json()
    assert data['id'] == resource_id, "Error: El ID del post no coincide"
    assert 'title' in data, "Error: Falta el campo 'title'"
    
    print("\n[INFO API] Test GET exitoso: Recurso obtenido correctamente.")


def test_02_post_create_resource():
    """
    CONSIGNA: Prueba POST - Crear un nuevo recurso y verificar el Status 201 y los datos de respuesta.
    Endpoint: /posts
    """
    endpoint = f"{BASE_URL}/posts"
    new_data = {
        "title": "Prueba de Integración Final",
        "body": "Contenido del post creado por Ezequiel",
        "userId": 1
    }
    
    logging.info(f"Enviando solicitud POST a: {endpoint} con datos: {new_data['title']}")
    response = requests.post(endpoint, json=new_data)
    
    # 1. Validar el Status Code (201 Created)
    assert response.status_code == 201, f"Error: Se esperaba Status 201, se obtuvo {response.status_code}"
    logging.info(f"Status Code 201 CREATED obtenido.")
    
    # 2. Validar la respuesta JSON
    response_data = response.json()
    assert response_data['title'] == new_data['title'], "Error: El título devuelto no coincide"
    assert response_data['userId'] == new_data['userId'], "Error: El userId devuelto no coincide"
    assert 'id' in response_data, "Error: La respuesta no contiene un ID generado"
    
    print(f"\n[INFO API] Test POST exitoso: Recurso creado con ID: {response_data['id']}.")


def test_03_put_update_resource():
    """
    CONSIGNA: Prueba PUT - Actualizar un recurso existente y verificar el Status 200.
    Endpoint: /posts/1
    """
    resource_id = 1
    endpoint = f"{BASE_URL}/posts/{resource_id}"
    updated_data = {
        "id": resource_id,
        "title": "Titulo Actualizado por PUT",
        "body": "El cuerpo ha sido modificado en la prueba PUT",
        "userId": 1
    }
    
    logging.info(f"Enviando solicitud PUT a: {endpoint}")
    response = requests.put(endpoint, json=updated_data)
    
    # 1. Validar el Status Code (200 OK)
    assert response.status_code == 200, f"Error: Se esperaba Status 200, se obtuvo {response.status_code}"
    logging.info(f"Status Code 200 OK obtenido.")
    
    # 2. Validar la respuesta JSON
    response_data = response.json()
    assert response_data['title'] == updated_data['title'], "Error: El título no se actualizó correctamente"
    
    print("\n[INFO API] Test PUT exitoso: Recurso actualizado correctamente.")