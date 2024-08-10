import requests
import configparser
import os

config = configparser.ConfigParser()

config_file = 'config.ini'

if not os.path.isfile(config_file):
    raise FileNotFoundError(f"El archivo de configuración {config_file} no se encuentra.")

config.read(config_file)

url_server = config.get('server', 'url_server')

def send_data_to_api(trash_type):
    """Envía datos sobre el tipo de basura a la API."""
    try:
        # Enviar datos a la API
        response = requests.post(url_server, json={"type": trash_type})
        
        # Verificar la respuesta
        if response.status_code == 200:
            response_data = response.json()
            print(f"Data sent successfully: {response_data}")
        else:
            print(f"Failed to send data: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data to API: {e}")