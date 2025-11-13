from fastapi import FastAPI, Header, HTTPException
from typing import Any
import os


def register(app: FastAPI, Req, ALLOWED, GEN_MODEL_MODE, GEN_MODEL_NAME, ollama_generate, hf_inference, extract_generated_text, parse_generated_field, is_probable_prompt_echo):

    @app.post("/analyze")
    def analyze(req: Any, api_key: str = Header(None, alias="api-key")):
        # Convert incoming body to Req if needed
        if not isinstance(req, Req):
            try:
                req = Req.parse_obj(req)
            except Exception:
                req = type("_R", (), {"text": (req.get("text") if isinstance(req, dict) else ""), "meta": {}})()

        if api_key not in ALLOWED:
            raise HTTPException(status_code=401, detail="Unauthorized")

        text = req.text or ""
        response_mode = req.meta.get("response_mode", "empathetic")
        gen_params = {
            "max_new_tokens": int(os.getenv("GEN_MAX_TOKENS", "200")),
            "temperature": float(os.getenv("GEN_TEMPERATURE", "0.6")),
        }

        if response_mode == "empathetic":
            prompt_empathetic = f"""Paciente: {text}

Você é um psicólogo clínico experiente. Responda ao paciente em português, de forma empática,
acolhedora e profissional. Faça:
1) 1-2 frases de acolhimento (empatia);
2) 2 sugestões práticas imediatas e seguras;
3) instrução de procurar ajuda/emergência se necessário;
Identifique o que a pessoa precisa. Responda em texto corrido, sem apresentar o prompt ou explicações sobre o que fez.
Não diga listas numeradas, apenas frases conectadas.
Não enumere itens

Seja breve, claro e direto
"""
            if GEN_MODEL_MODE == "local":
                gen_text = ollama_generate(prompt_empathetic, model=GEN_MODEL_NAME)
            else:
                try:
                    gen = hf_inference(GEN_MODEL_NAME, prompt_empathetic, params=gen_params)
                except HTTPException:
                    raise
                gen_text = extract_generated_text(gen)

            if is_probable_prompt_echo(prompt_empathetic, gen_text) or (isinstance(gen_text, str) and text.strip() in gen_text):
                fallback_prompt = f"""{text}

Responda ao paciente em português com uma mensagem curta, empática e direta (3-5 frases)."""
                if GEN_MODEL_MODE == "local":
                    try:
                        gen_text_fb = ollama_generate(fallback_prompt, model=GEN_MODEL_NAME)
                        if isinstance(gen_text_fb, str) and len(gen_text_fb.strip()) > 5:
                            gen_text = gen_text_fb
                    except Exception:
                        pass
                else:
                    try:
                        gen_fb = hf_inference(GEN_MODEL_NAME, fallback_prompt, params={"temperature": 0.7, "max_new_tokens": 120})
                        gen_text_fb = extract_generated_text(gen_fb)
                        if isinstance(gen_text_fb, str) and len(gen_text_fb.strip()) > 5:
                            gen_text = gen_text_fb
                    except HTTPException:
                        pass

            final_generated = gen_text

            if is_probable_prompt_echo(prompt_empathetic, final_generated) or (isinstance(final_generated, str) and text.strip() in final_generated):
                final_generated = (
                    "Sinto muito que você esteja se sentindo triste. "
                    "Estou aqui para ouvir. Uma sugestão: tente respirar profundamente por um minuto e anotar como se sente. "
                    "Se estiver em risco ou a situação piorar, procure ajuda profissional ou serviços de emergência."
                )

        else:
            prompt_structured = f"""Você é um psicólogo especialista. Recebe o texto do paciente abaixo.
Gere APENAS um JSON válido em português com as chaves:
- summary: string (1-2 frases)
- evidence: array de 2 strings (trechos do texto)
- hypotheses: array de 2 strings (hipóteses clínicas curtas)
- recommendations: array de 3 strings (ações práticas)
- suggested_questions: array de 3 strings (perguntas para a próxima sessão)

Texto do paciente:
<<<BEGIN_TEXT>>>
{text}
<<<END_TEXT>>>

Retorne apenas JSON válido (sem texto adicional).
"""
            if GEN_MODEL_MODE == "local":
                gen_text = ollama_generate(prompt_structured, model=GEN_MODEL_NAME)
            else:
                try:
                    gen = hf_inference(GEN_MODEL_NAME, prompt_structured, params=gen_params)
                except HTTPException:
                    raise
                gen_text = extract_generated_text(gen)

            parsed_gen, parse_err = parse_generated_field(gen_text)
            final_generated = parsed_gen if parsed_gen is not None else gen_text

            if is_probable_prompt_echo(prompt_structured, final_generated):
                final_generated = {
                    "summary": "Usuário relata sentir-se triste.",
                    "evidence": [text[:120], text[:120]],
                    "hypotheses": ["Tristeza situacional", "Possível alteração de humor"],
                    "recommendations": [
                        "Respirar profundamente por alguns minutos",
                        "Fazer uma caminhada curta",
                        "Procurar contato com pessoa de confiança ou profissional"
                    ],
                    "suggested_questions": [
                        "Quando começou esse sentimento?",
                        "Há algo que costuma ajudar quando se sente assim?",
                        "Você tem alguém com quem conversar no momento?"
                    ]
                }

        return {"generated": final_generated}
