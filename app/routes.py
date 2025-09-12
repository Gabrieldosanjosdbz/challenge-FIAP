from .models import AnaliseRequest, ResponseOutput
from .llm_service import analisar_painel
from .database import collection
from datetime import datetime, timezone
import json

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def ping():
    return {
        "message": "API rodando!",
        "timestamp": datetime.now(timezone.utc)
    }

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