from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException

from models.reserva import ReservaInput, ReservaOutput

router = APIRouter()

reservas = [
    {
        "id": 1,
        "mesa": 5,
        "nome": "Silva",
        "pessoas": 4,
        "data_hora": "2026-03-11T20:00:00",
        "ativa": True,
        "criada_em": "2026-03-10T09:00:00",
    },
    {
        "id": 2,
        "mesa": 3,
        "nome": "Costa",
        "pessoas": 2,
        "data_hora": "2026-03-12T19:30:00",
        "ativa": False,
        "criada_em": "2026-03-10T09:05:00",
    },
]

@router.get("/", response_model=list[ReservaOutput])
async def listar_reservas(data: Optional[str] = None, apenas_ativas: bool = True):
    resultado = reservas
    if apenas_ativas:
        resultado = [reserva for reserva in resultado if reserva["ativa"]]
    if data:
        resultado = [
            reserva
            for reserva in resultado
            if datetime.fromisoformat(reserva["data_hora"]).date().isoformat() == data
        ]
    return resultado


@router.post("/", response_model=ReservaOutput)
async def criar_reserva(reserva: ReservaInput):
    data_reserva = reserva.data_hora.date()
    conflito = any(
        item["mesa"] == reserva.mesa
        and item["ativa"]
        and datetime.fromisoformat(item["data_hora"]).date() == data_reserva
        for item in reservas
    )
    if conflito:
        raise HTTPException(
            status_code=400,
            detail=f"Mesa {reserva.mesa} já está reservada para {data_reserva.isoformat()}",
        )

    nova_reserva = {
        "id": len(reservas) + 1,
        "mesa": reserva.mesa,
        "nome": reserva.nome,
        "pessoas": reserva.pessoas,
        "data_hora": reserva.data_hora.isoformat(),
        "ativa": True,
        "criada_em": datetime.now().isoformat(),
    }
    reservas.append(nova_reserva)
    return nova_reserva


@router.get("/mesa/{numero}", response_model=list[ReservaOutput])
async def reservas_por_mesa(numero: int):
    return [reserva for reserva in reservas if reserva["mesa"] == numero]


@router.get("/{reserva_id}", response_model=ReservaOutput)
async def buscar_reserva(reserva_id: int):
    for reserva in reservas:
        if reserva["id"] == reserva_id:
            return reserva
    raise HTTPException(status_code=404, detail="Reserva não encontrada")


@router.delete("/{reserva_id}")
async def cancelar_reserva(reserva_id: int):
    for reserva in reservas:
        if reserva["id"] == reserva_id:
            if not reserva["ativa"]:
                raise HTTPException(status_code=400, detail="Reserva já está cancelada")
            reserva["ativa"] = False
            return {"mensagem": "Reserva cancelada com sucesso"}
    raise HTTPException(status_code=404, detail="Reserva não encontrada")
