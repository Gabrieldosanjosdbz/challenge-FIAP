from pydantic import BaseModel
from datetime import datetime

# aqui sera definido as request e responses da API
class AnaliseRequest(BaseModel):
    url: str               

class ResponseOutput(BaseModel):
    status: str
    url: str
    need_cleaning: bool       
    solar_level: int
    response: str      
    date_time: datetime  

class Entrada(BaseModel):
    url: str

class Saida(BaseModel):
    id: int
    needCleaning: bool
    nivelSolar: int
    analise: str

class Analise(BaseModel):
    id: ObjectIdField = Field(alias="_id")
    entrada: Entrada
    saida: Saida
    timestamp: datetime
