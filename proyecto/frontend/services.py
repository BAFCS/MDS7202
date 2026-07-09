from dotenv import load_dotenv
import random
from datetime import datetime
import requests 
import os

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")

def enviar_prediccion(Asunto_Ticket, Contenido_Ticket, Canal_Ticket, Categoría_Problema, Usuario_Tipo_de_Cuenta,  Usuario_Antiguedad_Cuenta_Dias):
    Id_Ticket = f"TCK-{random.randint(10000, 99999)}"  #Definimos la id del ticket sin necesidad del usuario
    fecha_envio = datetime.now().strftime("%Y-%m-%d")

    formato_json_entrada = {
    "Id_Ticket": Id_Ticket,
    "Asunto_Ticket": Asunto_Ticket,
    "Contenido_Ticket": Contenido_Ticket,
    "Canal_Ticket": Canal_Ticket,
    "Categoría_Problema": Categoría_Problema,
    "Usuario_Tipo_de_Cuenta": Usuario_Tipo_de_Cuenta,
    "Usuario_Antiguedad_Cuenta_Dias": Usuario_Antiguedad_Cuenta_Dias,
    "Fecha_Envío": fecha_envio
    }

    try:
        response = requests.post(f"{BACKEND_URL}/predict", json=formato_json_entrada)
        if response.status_code == 200:
            resultado = response.json()
            return resultado['Id_Ticket'], resultado['Prioridad']

        elif response.status_code == 422:
            print("Error 422, error de tipeo para la validación estricta")
        else:
            print("error del backend para conectarse")
    except requests.exceptions.ConnectionError as e:
        return f"No se pudo conectar al backend: {str(e)}"



