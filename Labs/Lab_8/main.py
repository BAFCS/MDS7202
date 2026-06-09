import os
import pickle
import fastapi
from mlflow import data
from setuptools import glob
import uvicorn
from fastapi.responses import JSONResponse  
import numpy as np
from pydantic import BaseModel

app = fastapi.FastAPI()

#Get default
@app.get("/")
def index():
    return {"message": "Bienvenido a la parte de FastAPI del lab_8"}


@app.get("/home")
def home():
    data = {
        "mensaje": "Bienvenido a la API de Potabilidad del Agua",
        "problema": "Prediccción de la potabilidad del agua (Clasificación Binaria) según la información del agua.",
        "modelo": "XGBoost, el cual es un algoritmo de aprendizaje supervisado basado en árboles de decisión que trabaja mediante una estrategia de crecimiento por niveles (level-wise), evaluando y dividiendo los nodos hoja de un nivel antes de pasar al siguiente, controlado por una profundidad máxima (max_depth) y técnicas de poda para evitar el sobreajuste.",        "optimizacion_hiperparametros": {
        "herramienta de optimización de hiperparámetros": "Optuna (15 iteraciones usando búsqueda bayesiana)",
                    "espacio_busqueda": {
                        "n_estimators": "Desde 50 hasta 200",
                        "max_depth": "Desde 3 hasta 10",
                        "learning_rate": "Desde 0.01 hasta 0.3"
                    }
        },
        "seguimiento": "MLflow para el seguimiento de los experimentos, guardando métricas, parámetros y modelos entrenados.",
        "entradas": [
            "pH", "Hardness", "Solids", "Chloramines", "Sulfate", "Conductivity", "Organic_carbon", "Trihalomethanes", "Turbidity",
        ],
        "salida": "Variable binaria (1: Potable, 0: No potable)",
        "detalles_entrenamiento": {
            "split": "80% entrenamiento, 20% prueba",
            "metrica_evaluacion": "F1-Score (media armónica entre la precisión y el recall) por clases desbalanceadas"
        }
    }
    return JSONResponse(content=data, media_type="application/json; charset=utf-8") #Para no tener problemas con caracteres especiales en la respuesta JSON, como los tildes


#Carga del modelo
MODELS_DIR = "models"
#Se busca todos los archivos .pkl dentro de models
pkl_files = glob.glob(os.path.join(MODELS_DIR, "*.pkl"))
if pkl_files:
    # Ordenar los archivos por su fecha de creación y se toma el más nuevo
    MODEL_PATH = max(pkl_files, key=os.path.getctime)
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    print(f"¡Modelo más reciente cargado exitosamente desde '{MODEL_PATH}'!")
else:
    model = None
    MODEL_PATH = None
    print(f"Advertencia: No se encontró ningún archivo .pkl en la carpeta '{MODELS_DIR}'.")

class MedicionAgua(BaseModel):
    ph: float
    Hardness: float
    Solids: float
    Chloramines: float
    Sulfate: float
    Conductivity: float
    Organic_carbon: float
    Trihalomethanes: float
    Turbidity: float


@app.post("/potabilidad/")
def predecir_potabilidad(data: MedicionAgua):
    features = np.array([
        data.ph,
        data.Hardness,
        data.Solids,
        data.Chloramines,
        data.Sulfate,
        data.Conductivity,
        data.Organic_carbon,
        data.Trihalomethanes,
        data.Turbidity
    ]).reshape(1, -1) #Convertimos la lista de características en un array de numpy y lo redimensionamos a una matriz de 1 fila y n columnas (donde n es el número de características)

    print("Esto es la data:", features)


    # Aqui se lee el modelo entrenado y se hace la prediccion con los datos recibidos
    prediccion_array = model.predict(features)
    resultado_final = int(prediccion_array[0]) #valor de la prediccion convertido a entero (0 o 1)

    return {"potabilidad": resultado_final}


#  Bloque para levantar el servidor ejecutando "python main.py"
if __name__ == "__main__":
    import uvicorn
    # Corre uvicorn apuntando a este mismo archivo ("main:app") en el puerto por defecto (8000)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

