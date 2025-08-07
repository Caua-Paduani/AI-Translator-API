
from fastapi import FastAPI, HTTPException
import requests
import re
import time
import os

cache = {}
CACHE_DURATION = 3600 # 1 hour

app = FastAPI()

def validate_cep(cep: str) -> str:
    cep_limpo = re.sub(r'\D', '', cep)
    if len(cep_limpo) != 8:
        raise HTTPException(status_code=400, detail="CEP deve ter 8 dígitos")
    return cep_limpo

        

@app.get("/buscar-cep")
async def buscar_cep(cep: str):
    cep_limpo = validate_cep(cep)
    agora = time.time()
    #verifica se o cep está no cache
    if cep_limpo in cache and agora - cache[cep_limpo]['timestamp'] < CACHE_DURATION:
        return cache[cep_limpo]['data']
    #se não estiver, busca no viacep
    url = f"https://viacep.com.br/ws/{cep_limpo}/json/"
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "CEP não encontrado"}
    dados = response.json()
    
    return dados 
