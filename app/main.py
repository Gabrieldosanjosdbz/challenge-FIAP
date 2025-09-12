from fastapi import FastAPI, Depends
from .auth import verify_bearer_token, ForceJSONMiddleware
from .routes import router as analisar_router

# ligar ambiente: source bin/activate
# desligar: deactivate
# rodar projeto: uvicorn app.main:app --reload
# pip install -r requirements.txt

app = FastAPI(
    title="Faculdade API",
    dependencies=[Depends(verify_bearer_token)]
)

app.add_middleware(ForceJSONMiddleware)

app.include_router(analisar_router, prefix="/challenge")
