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
        response_mode = req.meta.get("response_mode", "empathetic")

        if response_mode == "empathetic":
            prompt = f"""Paciente: {text}

Você é um psicólogo clínico experiente. Responda ao paciente em português, de forma empática, acolhedora e profissional. Faça:
1)Frases de acolhimento (empatia);
2)Sugestões práticas imediatas e seguras;
3) instrução de procurar ajuda/emergência se necessário;
Identifique o que a pessoa precisa. Responda em texto corrido, sem apresentar o prompt ou explicações sobre o que fez.
Não diga listas numeradas, apenas frases conectadas.
Não enumere itens
Seja breve, claro e direto
Você deve ajudar a pessoa a se sentir melhor e segura.
"""
        else:
            prompt = f"""
Paciente: {text}

Você é um psicólogo clínico experiente e empático. Responda em português, com acolhimento genuíno e linguagem simples. 
Sua resposta deve transmitir calma, segurança e compreensão. 

Objetivos:
- Acolha o que a pessoa sente, demonstrando empatia e escuta genuína.
- Ofereça orientações práticas e seguras que possam ajudar no momento.
- Incentive a buscar apoio profissional ou serviços de emergência se houver risco imediato.

Regras:
- Escreva em texto corrido, sem listas, tópicos ou numeração.
- Seja breve, direto e humano, sem repetir o texto do paciente.
- Não explique o que está fazendo, apenas responda de forma natural e acolhedora.
- Mantenha sempre um tom de apoio emocional, empatia e segurança.
- Se identificar sinais de perigo iminente (como risco de suicídio, automutilação ou violência), oriente de forma clara e cuidadosa para que a pessoa procure ajuda humana imediata — como familiares, amigos de confiança, um profissional de saúde mental ou o serviço de emergência local (como o 188 no Brasil).
"""

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

        return {"generated": result}
