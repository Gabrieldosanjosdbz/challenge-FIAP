import os
from dotenv import load_dotenv
from fastapi import Header, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

def verify_bearer_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token inválido")
    token = authorization.split(" ")[1]
    if token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido")
    return True

class ForceJSONMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Content-Type"] = "application/json"
        return response