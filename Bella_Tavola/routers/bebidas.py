from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException

from models.bebida import BebidaInput, BebidaOutput


router = APIRouter()

bebidas = [
    {
        "id": 1,
        "nome": "Água Mineral",
        "tipo": "agua",
        "preco": 8.0,
        "alcoolica": False,
        "volume_ml": 500,
        "criado_em": "2024-01-01T00:00:00",
    },
    {
        "id": 2,
        "nome": "Chianti Classico",
        "tipo": "vinho",
        "preco": 120.0,
        "alcoolica": True,
        "volume_ml": 750,
        "criado_em": "2024-01-01T00:00:00",
    },
    {
        "id": 3,
        "nome": "San Pellegrino",
        "tipo": "agua",
        "preco": 15.0,
        "alcoolica": False,
        "volume_ml": 750,
        "criado_em": "2024-01-01T00:00:00",
    },
    {
        "id": 4,
        "nome": "Suco de Laranja",
        "tipo": "suco",
        "preco": 18.0,
        "alcoolica": False,
        "volume_ml": 300,
        "criado_em": "2024-01-01T00:00:00",
    },
    {
        "id": 5,
        "nome": "Prosecco",
        "tipo": "vinho",
        "preco": 95.0,
        "alcoolica": True,
        "volume_ml": 750,
        "criado_em": "2024-01-01T00:00:00",
    },
]


@router.get("/")
async def listar_bebidas(tipo: Optional[str] = None, alcoolica: Optional[bool] = None):
    resultado = bebidas
    if tipo:
        resultado = [bebida for bebida in resultado if bebida["tipo"] == tipo]
    if alcoolica is not None:
        resultado = [bebida for bebida in resultado if bebida["alcoolica"] == alcoolica]
    return resultado


@router.get("/{bebida_id}")
async def buscar_bebida(bebida_id: int):
    for bebida in bebidas:
        if bebida["id"] == bebida_id:
            return bebida
    raise HTTPException(
        status_code=404,
        detail=f"Bebida com id {bebida_id} não encontrada",
    )


@router.post("/", response_model=BebidaOutput)
async def criar_bebida(bebida: BebidaInput):
    novo_id = max(item["id"] for item in bebidas) + 1
    nova_bebida = {
        "id": novo_id,
        "criado_em": datetime.now().isoformat(),
        **bebida.model_dump(),
    }
    bebidas.append(nova_bebida)
    return nova_bebida
