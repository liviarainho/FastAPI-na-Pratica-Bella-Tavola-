from typing import Optional

from pydantic import BaseModel, Field, field_validator


class PratoInput(BaseModel):
    nome: str = Field(min_length=3, max_length=100)
    categoria: str = Field(pattern="^(pizza|massa|sobremesa|entrada|salada)$")
    preco: float = Field(gt=0)
    preco_promocional: Optional[float] = Field(default=None, gt=0)
    descricao: Optional[str] = Field(default=None, max_length=500)
    disponivel: bool = True

    @field_validator("preco_promocional")
    @classmethod
    def validar_preco_promocional(cls, value, info):
        if value is None:
            return value
        if "preco" not in info.data:
            return value

        preco_original = info.data["preco"]
        if value >= preco_original:
            raise ValueError("Preço promocional deve ser menor que o preço original")

        desconto = (preco_original - value) / preco_original
        if desconto > 0.5:
            raise ValueError("Desconto não pode ser maior que 50% do preço original")

        return value


class PratoOutput(BaseModel):
    id: int
    nome: str
    categoria: str
    preco: float
    descricao: Optional[str] = None
    disponivel: bool
    criado_em: str


class DisponibilidadeInput(BaseModel):
    disponivel: bool

