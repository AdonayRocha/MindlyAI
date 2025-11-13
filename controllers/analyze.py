from fastapi import Header, HTTPException
import os
from groq import Groq
from models.req import Req

def register(app, ALLOWED):
    @app.post("/analyze")
    def analyze(req: Req, api_key: str = Header(None, alias="api-key")):
        if api_key not in ALLOWED:
            raise HTTPException(status_code=401, detail="Unauthorized")

        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        if not GROQ_API_KEY:
            raise HTTPException(status_code=500, detail="GROQ_API_KEY não configurada.")

        client = Groq(api_key=GROQ_API_KEY)
        text = req.text or ""
        response_mode = req.meta.get("response_mode", "insight")

        if response_mode == "insight":
            prompt = f"""Texto do paciente: {text}

Você é um psicólogo clínico experiente. Analise o texto acima e gere INSIGHTS para o psicólogo sobre pontos de atenção, possíveis focos para trabalhar, sinais de risco, temas recorrentes e sugestões de abordagem.

Regras:
- Escreva em português, de forma clara, profissional e direta.
- Não repita o texto do paciente.
- Não escreva para o paciente, escreva para o psicólogo.
- Destaque possíveis hipóteses, temas sensíveis, fatores de risco e oportunidades de intervenção.
- Seja breve, objetivo e prático.
- Não use listas numeradas, escreva em texto corrido.
- Não explique o que está fazendo, apenas traga os insights.
"""
        else:
            prompt = f"Texto do paciente: {text}\n\nGere insights clínicos para o psicólogo."

        messages = [
            {"role": "user", "content": prompt}
        ]

        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            temperature=1,
            max_completion_tokens=8192,
            top_p=1,
            reasoning_effort="medium",
            stream=True,
            stop=None
        )

        result = ""
        for chunk in completion:
            result += chunk.choices[0].delta.content or ""

        return {"insights": result}

