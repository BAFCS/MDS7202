from pydantic import BaseModel



class PredictionRequest(BaseModel):
    Id_Ticket: str
    Asunto_Ticket: str
    Contenido_Ticket: str
    Canal_Ticket: str
    Categoría_Problema: str
    Usuario_Tipo_de_Cuenta: str
    Usuario_Antiguedad_Cuenta_Dias: int
    Fecha_Envío: str

class PredictionResponse(BaseModel):
    Id_Ticket: str
    Prioridad: str


