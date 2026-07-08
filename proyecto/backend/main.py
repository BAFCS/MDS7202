from generate_prediction import generate_prediction
import os
import pickle
import pandas as pd
import fastapi
from fastapi import HTTPException
import numpy as np
import uvicorn
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from setuptools import glob

from models import PredictionRequest, PredictionResponse
from pydantic import ValidationError

app = fastapi.FastAPI()

# Get default
@app.get("/")
def index():
    return {"message": "Bienvenido a la aplicación de predicción de la prioridad del ticket para ChaucherApp. Esta aplicación permitirá automatizar la categorización y permitirá priorizar tickets Críticos rapidamente"}

@app.post("/predict", response_model=PredictionResponse)
def predict(data: PredictionRequest):
    print(data)
    data_df = pd.DataFrame([data.model_dump()])
    try:
        predicciones = generate_prediction(data_df)
        print(predicciones)

        return PredictionResponse(
            Id_Ticket=str(predicciones['Id_Ticket'].iloc[0]),
            Prioridad=str(predicciones['Prediccion'].iloc[0])
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno en la predicción: {str(e)}"
        )



#  Bloque para levantar el servidor ejecutando "python main.py"
if __name__ == "__main__":
    import uvicorn

    # Corre uvicorn apuntando a este mismo archivo ("main:app") en el puerto por defecto (8000)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


#Para ejecutar uvicorn backend.main:app --reload