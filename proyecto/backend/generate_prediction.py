# %%
import pandas as pd
import pickle
from dotenv import load_dotenv
import numpy as np
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

MODEL_PATH = "modelo_final.pkl"

# %%
def generate_prediction(df) -> str:
    df_new = df.copy()
    df_new["Texto"] = df_new["Asunto_Ticket"].fillna("") + " " + df_new["Contenido_Ticket"].fillna("")
    df_new['N_Caracteres_Ticket'] = (
    df_new["Texto"].str.replace(r"[\r\n]", " ", regex=True).str.strip().str.len() - 1
    )

    embeddings_model = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        output_dimensionality=1024
    )
    list_of_texts = df_new['Texto'].tolist()
    embeddings_list = embeddings_model.embed_documents(list_of_texts)

    df_embeddings = pd.DataFrame(embeddings_list)
    df_embeddings.columns = [f"embedding_dim_{i+1}" for i in range(df_embeddings.shape[1])]

    df_embeddings["Id_Ticket"] = df_new["Id_Ticket"].values

    X_full = pd.merge(
        df_new.drop(columns=["Asunto_Ticket", "Contenido_Ticket"]),
        df_embeddings,
        on="Id_Ticket",
    ).drop(columns=["Id_Ticket"])

    print("Cargando modelo .....")
    with open(MODEL_PATH, "rb") as f:
        pipeline_model = pickle.load(f)
    print("Carga modelo completado")

    print("Prediciendo ...")
    prediction = pipeline_model.predict(X_full)
    df_new['Prediccion'] = [str(p) for p in prediction]

    return df_new[['Id_Ticket', 'Prediccion']]


# %%
if __name__ == "__main__":
    print("--- Creando datos sintéticos de prueba ---")
    # Datos sintéticos idénticos a la estructura de tu ChaucherApp
    data = {
        "Id_Ticket": ["TCK-19267", "TCK-19268", "TCK-19263"],
        "Asunto_Ticket": [
            "Error al iniciar sesión en nuevo celular por d...",
            "Error al actualizar correo electrónico: bloqueado por seguridad",
            "Alerta de Fraude - Tarjeta bloqueada"
        ],
        "Contenido_Ticket": [
            "hola oye lo que pasa es que me cambie de celu ...",
            "Hola, buenas tardes. Escribo porque estoy tratando de actualizar mis datos personales en la aplicacion, especificamente el cambio de mi correo electronico porque el que tenia registrado ya no lo uso y se me perdio la clave. \r\n\r\nYa intente hacer el proceso desde el menu de configuracion, pero me aparece un mensaje que dice que los datos estan bloqueados por validacion de seguridad. Me gustaria saber que pasos debo seguir para poder actualizarlo o si necesito enviar algun documento adicional para verificar que soy el titular de la cuenta, ya que uso harto la tarjeta digital y me preocupa no recibir los comprobantes de las transferencias. \r\n\r\nQuedo atento a lo que me indiquen para poder solucionar esto pronto. Gracias.",
            "Me cobraron una compra de 500.000 CLP en un comercio que no conozco. ¡Necesito bloquear todo ya!"
        ],
        "Canal_Ticket": ["Whatsapp", "Whatsapp", "Página Web"],
        "Categoría_Problema": ["Cuenta", "Otro", "Fraude"],
        "Usuario-Tipo_de_Cuenta": ["Premium", "Premium", "Free"],
        "Usuario-Antiguedad_Cuenta_Dias": [159, 192, 232],
        "Fecha_Envío": ["2024-01-02", "2024-01-02", "2024-01-02"],
    }

    df_prueba = pd.DataFrame(data)

    predicciones =generate_prediction(df_prueba)

    print(predicciones)

