from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

app = FastAPI(
    title="InclusIA",
    version="0.2.0"
)


class Pergunta(BaseModel):
    mensagem: str


@app.get("/")
def inicio():
    return {
        "nome": "InclusIA",
        "mensagem": "Olá! Eu sou a InclusIA, sua assistente de Educação Inclusiva."
    }


@app.post("/chat")
def chat(pergunta: Pergunta):

    resposta = client.responses.create(
        model="gpt-5-mini",
        instructions=(
            "Você é a InclusIA, uma assistente especializada em "
            "Educação Inclusiva. Responda em português do Brasil, "
            "de forma clara, acolhedora e profissional. "
            "Não substitua profissionais especializados e não "
            "invente informações."
        ),
        input=pergunta.mensagem
    )

    return {
        "resposta": resposta.output_text
    }