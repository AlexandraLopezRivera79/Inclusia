from fastapi import FastAPI
from pydantic import BaseModel
import requests


app = FastAPI(
    title="InclusIA",
    version="0.3.0"
)


class Atividade(BaseModel):
    disciplina: str
    ano: str
    atividade: str
    necessidade: str


@app.get("/")
def inicio():
    return {
        "nome": "InclusIA",
        "mensagem": "Olá! Eu sou a InclusIA, sua assistente de Educação Inclusiva."
    }


@app.post("/chat")
def chat(atividade: Atividade):

    prompt = f"""
Você é a InclusIA, uma assistente de Educação Inclusiva.

Responda em português do Brasil, de forma clara, acolhedora e profissional.

Sua função é auxiliar professores e profissionais da educação na adaptação
de atividades pedagógicas.

Não substitua a avaliação de profissionais especializados.
Não invente informações sobre o estudante.

Analise a atividade abaixo:

Disciplina: {atividade.disciplina}
Ano: {atividade.ano}
Atividade: {atividade.atividade}
Necessidade educacional: {atividade.necessidade}

Forneça uma sugestão de adaptação pedagógica contendo:

1. Objetivo da atividade
2. Adaptação sugerida
3. Estratégia de aplicação
4. Recursos necessários
5. Forma de avaliação

A adaptação deve ser prática e adequada ao contexto escolar.
"""

    resposta = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:latest",
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    resposta.raise_for_status()

    dados = resposta.json()

    return {
        "resposta": dados["response"]
    }