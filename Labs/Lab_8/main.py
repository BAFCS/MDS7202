import os
import pickle

import fastapi
from mlflow import data
import uvicorn
from fastapi.responses import JSONResponse  # <-- 1. Importa esto

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
            "pH", "Dureza", "Solidos disueltos", "Concentración de cloraminas", 
            "Sulfatos", "Conductividad", "Carbono orgánico total", 
            "Trihalometanos", "Turbidez"
        ],
        "salida": "Variable binaria (1: Potable, 0: No potable)",
        "detalles_entrenamiento": {
            "split": "80% entrenamiento, 20% prueba",
            "metrica_evaluacion": "F1-Score (media armónica entre la precisión y el recall) por clases desbalanceadas"
        }
    }
    return JSONResponse(content=data, media_type="application/json; charset=utf-8") #Para no tener problemas con caracteres especiales en la respuesta JSON, como los tildes


#Carga del modelo
MODEL_PATH = os.path.join("models", "best_model.pkl")
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    print("Modelo cargado exitosamente desde '{}'!".format(MODEL_PATH))
else:
    model = None
    print(f"Advertencia: No se encontró el archivo del modelo en '{MODEL_PATH}'. Asegúrate de entrenarlo primero.")

@app.post("/potabilidad/")
def predecir_potabilidad(data: dict):

    # Aqui se lee el modelo entrenado y se hace la prediccion con los datos recibidos
    prediccion = model.predict(data)
    return {"prediccion": prediccion}


#  Bloque para levantar el servidor ejecutando "python main.py"
if __name__ == "__main__":
    import uvicorn
    # Corre uvicorn apuntando a este mismo archivo ("main:app") en el puerto por defecto (8000)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

