import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Casa de Sucos API")

URL = "https://www.fruityvice.com/api/fruit"

sucos = []


class SucoNovo(BaseModel):
    nome: str
    frutas: list[str]
    tem_gosto_de: str


def buscar_fruta(nome):
    resposta = requests.get(f"{URL}/{nome.lower()}")

    if resposta.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail=f"Fruta '{nome}' não encontrada.",
        )

    dados = resposta.json()
    return {
        "nome": dados["name"],
        "calorias": dados["nutritions"]["calories"],
        "acucar": dados["nutritions"]["sugar"],
    }


def calcular_totais(lista_de_frutas):
    total_calorias = 0
    total_acucar = 0

    for nome in lista_de_frutas:
        fruta = buscar_fruta(nome)
        total_calorias += fruta["calorias"]
        total_acucar += fruta["acucar"]

    return total_calorias, round(total_acucar, 2)


@app.get("/frutas/{nome}")
def consultar_fruta(nome: str):
    return buscar_fruta(nome)


@app.post("/sucos")
def cadastrar_suco(dados: SucoNovo):
    calorias, acucar = calcular_totais(dados.frutas)

    suco = {
        "id": len(sucos) + 1,
        "nome": dados.nome,
        "frutas": dados.frutas,
        "tem_gosto_de": dados.tem_gosto_de,
        "total_calorias": calorias,
        "total_acucar": acucar,
    }

    sucos.append(suco)
    return suco


@app.get("/sucos")
def listar_sucos():
    return sucos