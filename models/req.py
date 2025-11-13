"""
Modelo Req: estrutura de dados para requisições da API Mindly.

Este modelo é utilizado para validar e tipar o corpo das requisições recebidas nos endpoints,
garantindo que o JSON enviado pelo cliente tenha pelo menos o campo 'text' (string)
e, opcionalmente, um campo 'meta' (dicionário com informações adicionais).
"""
from pydantic import BaseModel

class Req(BaseModel):
    text: str
    meta: dict = {}
