from .models import AnaliseRequest, ResponseOutput, Analise, AnaliseCriadaResponse
from .llm_service import analisar_painel
from .database import collection
from datetime import datetime, timezone
from typing import List
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status
from bson import ObjectId #
from bson.errors import InvalidId
from fastapi import APIRouter

router = APIRouter()

def serialize_doc(doc):
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

@router.get("/")
def ping():
    return {
        "message": "API rodando!",
        "timestamp": datetime.now(timezone.utc)
    }

@router.get("/analises", response_model=List[Analise])
async def pegaAnalises():
    documentos = list(collection.find({})) # Converte o cursor para uma lista
    return documentos

@router.get("/analises/data/{data_str}", response_model=List[Analise])
def pega_analises_por_data(data_str: str):

    try:
        data_inicio = datetime.strptime(data_str, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de data inválido. Use AAAA-MM-DD."
        )

    data_fim = data_inicio + timedelta(days=1)

    query = {
        "timestamp": {
            "$gte": data_inicio,
            "$lt": data_fim
        }
    }

    documentos = list(collection.find(query).limit(1))


    if not documentos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nenhuma análise encontrada para a data {data_str}"
        )

    return documentos
@router.get("/analises/{item_id}")
def pega_analises_por_data(item_id: str):
    try:
        documento = collection.find_one({"_id": ObjectId(item_id)})
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID de item inválido")

    if not documento:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    return serialize_doc(documento)


@router.post("/analisar",response_model=AnaliseCriadaResponse)
async def analisar(input_data: AnaliseRequest):
    resultado = await analisar_painel(input_data.url)

    registro = {
        "entrada": input_data.model_dump(),
        "saida": resultado,
        "timestamp": datetime.now(timezone.utc)
    }
    result = collection.insert_one(registro)

    resposta = {
        "id": str(result.inserted_id),
        "resultado": resultado
    }

    return resposta