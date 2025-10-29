from pydantic import BaseModel
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from pydantic_mongo import ObjectIdField
from typing import Optional, List
from bson import ObjectId

# aqui sera definido as request e responses da API
class AnaliseRequest(BaseModel):
    url: str               

class ResponseOutput(BaseModel):
    id: ObjectIdField = Field(alias="_id")
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


class AnaliseRe0quest(BaseModel):
    url: str

class ResultadoAnalise(BaseModel):
    needCleaning: bool # Atenção ao case das chaves! O erro mostra 'needCleaning'
    nivelSolar: int
    analise: str

class AnaliseCriadaResponse(BaseModel):
    id: str
    resultado: ResultadoAnalise

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )
# class Analise(BaseModel):
#     id: ObjectIdField = Field(alias="_id")
#     url: str
#     needCleaning: bool
#     nivelSolar: int
#     analise: str
#     timestamp: datetime