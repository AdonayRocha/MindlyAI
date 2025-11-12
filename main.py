from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from dotenv import load_dotenv
import os, requests, json, logging
from typing import List, Tuple, Any, Optional
import re
from keywords.alerts import ALERTS
from keywords.topics import TOPIC_KEYWORDS

load_dotenv()

# Logging básico
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mindly")

# Variáveis de ambiente
HF_TOKEN = os.getenv("MINDLY_TOKEN")
if HF_TOKEN:
    logger.info("MINDLY_TOKEN carregado (tamanho=%d chars)", len(HF_TOKEN))
else:
    logger.warning("Aviso: MINDLY_TOKEN não encontrado nas variáveis de ambiente.")

EMOTION_MODEL = os.getenv("EMOTION_MODEL", "valhalla/distilbart-mnli-12-1")
GEN_MODEL_MODE = os.getenv("GEN_MODEL_MODE", "hf")     # "hf" ou "local"
GEN_MODEL_NAME = os.getenv("GEN_MODEL_NAME", "ssheifer/distilbart-cnn-12-6")
ALLOWED = os.getenv("API_KEYS", "meu_token").split(",")

HF_ROUTER = "https://router.huggingface.co/hf-inference/models/"
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "ollama")
OLLAMA_PORT = int(os.getenv("OLLAMA_PORT", "11434"))

app = FastAPI(title="Mindly")

class Req(BaseModel):
    text: str
    meta: dict = {}

# ---- Helpers -----------------------------------------------------------------------
def ollama_generate(prompt: str, model: str = None) -> str:
    """
    Chama Ollama local (container) para geração.
    Retorna string com a resposta ou lança HTTPException.
    """
    model = model or GEN_MODEL_NAME
    try:
        url = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/generate"
        payload = {"model": model, "prompt": prompt, "stream": False}
        r = requests.post(url, json=payload, timeout=120)
        r.raise_for_status()
        data = r.json()
        return data.get("response", "") or data.get("text", "")
    except Exception as e:
        logger.exception("Erro ao chamar Ollama: %s", e)
        raise HTTPException(status_code=500, detail="Erro ao gerar resposta com Ollama")

def hf_inference(model: str, inputs: str, params: dict = None) -> Any:
    """
    Chama Hugging Face Router Inference API.
    Retorna JSON parseado ou lança HTTPException com detalhe.
    """
    if not HF_TOKEN:
        raise HTTPException(status_code=500, detail="Hugging Face token não configurado (MINDLY_TOKEN).")
    url = HF_ROUTER + model
    headers = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}
    payload = {"inputs": inputs}
    if params:
        payload["parameters"] = params
    try:
        logger.info("Chamando HF model=%s url=%s params=%s", model, url, json.dumps(params or {}))
        r = requests.post(url, json=payload, headers=headers, timeout=40)
    except requests.RequestException as exc:
        logger.exception("Erro de conexão com Hugging Face: %s", exc)
        raise HTTPException(status_code=502, detail=f"Erro de conexão com Hugging Face: {exc}")

def normalize_emotion_response(resp: Any) -> List[dict]:
    if isinstance(resp, dict) and "labels" in resp and "scores" in resp:
        return [{"label": l, "score": float(s)} for l, s in zip(resp["labels"], resp["scores"]) ]
    if isinstance(resp, list) and len(resp) > 0 and isinstance(resp[0], dict) and "labels" in resp[0] and "scores" in resp[0]:
        return [{"label": l, "score": float(s)} for l, s in zip(resp[0]["labels"], resp[0]["scores"]) ]
    if isinstance(resp, list) and len(resp) > 0 and isinstance(resp[0], dict) and "label" in resp[0] and "score" in resp[0]:
        return [{"label": item["label"], "score": float(item["score"])} for item in resp]
    return []

def parse_generated_field(gen_field: Any) -> Tuple[Optional[Any], Optional[str]]:
    if isinstance(gen_field, (dict, list)):
        return gen_field, None
    if not isinstance(gen_field, str):
        return None, "Formato inesperado"
    try:
        obj = json.loads(gen_field)
        return obj, None
    except Exception:
        pass
    try:
        unescaped = gen_field.encode('utf-8').decode('unicode_escape')
        obj = json.loads(unescaped)
        return obj, None
    except Exception:
        pass
    return None, "Não foi possível parsear JSON; conteúdo: " + (gen_field[:300] if isinstance(gen_field, str) else str(gen_field))

def extract_generated_text(gen: Any) -> str:
    if isinstance(gen, list) and len(gen) > 0 and isinstance(gen[0], dict):
        return gen[0].get("generated_text") or gen[0].get("summary_text") or json.dumps(gen[0], ensure_ascii=False)
    if isinstance(gen, dict):
        return gen.get("generated_text") or gen.get("summary_text") or gen.get("raw") or json.dumps(gen, ensure_ascii=False)
    if isinstance(gen, str):
        parsed, err = parse_generated_field(gen)
        if parsed is not None:
            if isinstance(parsed, list) and len(parsed) > 0 and isinstance(parsed[0], dict):
                return parsed[0].get("generated_text") or parsed[0].get("summary_text") or json.dumps(parsed[0], ensure_ascii=False)
            if isinstance(parsed, dict):
                return parsed.get("generated_text") or parsed.get("summary_text") or json.dumps(parsed, ensure_ascii=False)
        return gen
    return json.dumps(gen, ensure_ascii=False)


def is_probable_prompt_echo(prompt: str, gen_text: Any) -> bool:
    try:
        if not isinstance(gen_text, str):
            gen_s = json.dumps(gen_text, ensure_ascii=False)
        else:
            gen_s = gen_text
        p = re.sub(r"\W+", " ", prompt.lower())
        g = re.sub(r"\W+", " ", gen_s.lower())
        p_words = [w for w in p.split() if len(w) > 2]
        if p_words:
            overlap = sum(1 for w in set(p_words) if w in g) / max(1, len(set(p_words)))
            if overlap >= 0.35:
                return True
        keywords = ["psicólogo", "responda", "faça", "faça:", "paciente", "acolh", "instru", "procure", "ajuda", "sugest"]
        if any(k in g for k in keywords):
            return True
    except Exception:
        return False
    return False

def detect_alerts(text: str) -> List[str]:
    return [w for w in ALERTS if w in text.lower()]

def simple_topic_extraction(text: str) -> List[str]:
    lowered = text.lower()
    topics = []
    for topic, kws in TOPIC_KEYWORDS.items():
        for k in kws:
            if k in lowered:
                topics.append(topic)
                break
    return topics

def compute_risk_basic(alerts: List[str], topics: List[str]) -> int:
    score = 0
    if alerts:
        score += 60
    score += len(topics) * 5
    return min(100, score)

@app.get("/health")
def health():
    return {"status": "Saudavel"}

@app.post("/detect")
def detect(req: Req):
    text = req.text or ""
    alerts = detect_alerts(text)
    topics = simple_topic_extraction(text)
    risk = compute_risk_basic(alerts, topics)
    return {
        "alert": bool(alerts),
        "alert_words": alerts,
        "topics": topics,
        "risk_score": risk
    }

@app.post("/analyze")
def analyze(req: Req, api_key: str = Header(None, alias="api-key")):
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