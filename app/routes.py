from .models import AnaliseRequest, ResponseOutput, Analise
from .llm_service import analisar_painel
from .database import collection
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, HTTPException, status
from typing import List

router = APIRouter()

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


@router.post("/analisar")
async def analisar(input_data: AnaliseRequest):
    resultado = await analisar_painel(input_data.url)

    registro = {
        "entrada": input_data.model_dump(),
        "saida": resultado,
        "timestamp": datetime.now(timezone.utc)
    }
    collection.insert_one(registro)

    return ResponseOutput(
        status="success",
        url=input_data.url,
        need_cleaning=resultado.get("needCleaning", False),
        solar_level= resultado.get("nivelSolar", 0),
        response=resultado.get("analise", ""),
        date_time=datetime.now(timezone.utc)
    )