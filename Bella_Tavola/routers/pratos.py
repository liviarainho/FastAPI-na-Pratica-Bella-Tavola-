from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException

from models.prato import DisponibilidadeInput, PratoInput, PratoOutput


router = APIRouter()

pratos = [
    {"id": 1, "nome": "Margherita", "categoria": "pizza", "preco": 45.0, "disponivel": True},
    {"id": 2, "nome": "Carbonara", "categoria": "massa", "preco": 52.0, "disponivel": True},
    {"id": 3, "nome": "Lasanha Bolonhesa", "categoria": "massa", "preco": 58.0, "disponivel": False},
    {"id": 4, "nome": "Tiramisù", "categoria": "sobremesa", "preco": 28.0, "disponivel": True},
    {"id": 5, "nome": "Quattro Stagioni", "categoria": "pizza", "preco": 49.0, "disponivel": True},
    {"id": 6, "nome": "Panna Cotta", "categoria": "sobremesa", "preco": 24.0, "disponivel": True},
]


@router.get("/")
async def listar_pratos(
    categoria: Optional[str] = None,
    preco_maximo: Optional[float] = None,
    apenas_disponiveis: bool = False,
):
    resultado = pratos
    if categoria:
        resultado = [prato for prato in resultado if prato["categoria"] == categoria]
    if preco_maximo is not None:
        resultado = [prato for prato in resultado if prato["preco"] <= preco_maximo]
    if apenas_disponiveis:
        resultado = [prato for prato in resultado if prato["disponivel"]]
    return resultado


@router.get("/{prato_id}")
async def buscar_prato(prato_id: int, formato: str = "completo"):
    for prato in pratos:
        if prato["id"] == prato_id:
            if formato == "resumido":
                return {"nome": prato["nome"], "preco": prato["preco"]}
            return prato
    raise HTTPException(
        status_code=404,
        detail=f"Prato com id {prato_id} não encontrado",
    )


@router.post("/", response_model=PratoOutput)
async def criar_prato(prato: PratoInput):
    novo_id = max(item["id"] for item in pratos) + 1
    novo_prato = {
        "id": novo_id,
        "criado_em": datetime.now().isoformat(),
        **prato.model_dump(),
    }
    pratos.append(novo_prato)
    return novo_prato


@router.put("/{prato_id}/disponibilidade")
async def alterar_disponibilidade(prato_id: int, body: DisponibilidadeInput):
    for prato in pratos:
        if prato["id"] == prato_id:
            prato["disponivel"] = body.disponivel
            return prato
    raise HTTPException(status_code=404, detail="Prato não encontrado")
