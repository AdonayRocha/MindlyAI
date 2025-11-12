# Mindly — mini ambiente

Este repositório contém uma API FastAPI chamada `mindly` para análise curta de textos (detecção de alertas, extração de tópicos, detecção de emoção e geração de respostas empáticas ou estruturadas). O projeto pode usar modelos hospedados no Hugging Face (via Router Inference) ou um servidor local Ollama para geração de texto.

Conteúdo principal
- `main.py` — aplicação FastAPI com endpoints `/health`, `/detect` e `/analyze`.
- `requirements.txt` — dependências Python.
- `Dockerfile` — imagem para rodar a aplicação.
- `docker-compose.yml` — orquestra o serviço `mindly`; o compose está preparado para conectar a um serviço `ollama` rodando separadamente (ou o host).
- `.env` — configurações e tokens (não comitar). Veja `.env` para exemplos.

Pré-requisitos
- Docker e Docker Compose (recomendado para replicar o ambiente com Ollama).
- Python 3.11 (se optar por rodar localmente sem Docker).

Configuração inicial (primeira vez)
1. Faça um clone do repositório e entre na pasta:

```powershell
git clone <repo-url>
cd MindlyAI
```

2. Crie um arquivo `.env` a partir do modelo e preencha as variáveis necessárias (não compartilhe o token publicamente):

```powershell
copy .env.example .env
# edite .env e preencha MINDLY_TOKEN e outras variáveis conforme necessário
```

3. Escolha o modo de execução:

- Usando Docker Compose (recomendado): sobe a API e conecta ao Ollama externo/host.
- Rodando localmente em Python: útil para desenvolvimento sem containers.

Executando com Docker Compose (recomendado)

No PowerShell:

```powershell
# Subir o serviço mindly (em background)
docker compose up -d --build

# Ver logs em tempo real
docker compose logs -f mindly
```

Observações para Windows: se você usa Ollama instalado no host e o `mindly` executar em container, ajuste `OLLAMA_HOST=host.docker.internal` no `.env` para que o container consiga se conectar ao serviço Ollama do host.

Executando localmente (sem Docker)

```powershell
# Crie e ative um virtualenv (PowerShell)
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Inicie a API
uvicorn main:app --host 0.0.0.0 --port 8000
```

Como o serviço funciona
- `/health` — retorna status simples da aplicação.
- `/detect` — recebe JSON com `{ "text": "..." }` e retorna detecção de palavras de alerta, tópicos e uma pontuação de risco básica (sem chamadas a modelos externos).
- `/analyze` — recebe `{ "text": "...", "meta": { ... } }` e executa:
  1. Detecção de emoções (zero-shot) usando o modelo definido em `EMOTION_MODEL` via Hugging Face Router (requer `MINDLY_TOKEN`).
  2. Cálculo de risco baseado em palavras de alerta e probabilidades de emoções.
  3. Geração de resposta — pode ser modo `empathetic` (texto livre) ou `structured` (JSON estruturado). A geração usa um dos dois mecanismos:
     - Hugging Face Router Inference (`GEN_MODEL_MODE=hf`) — precisa de `MINDLY_TOKEN`.
     - Ollama local (`GEN_MODEL_MODE=local`) — faz POST para `http://<OLLAMA_HOST>:<OLLAMA_PORT>/api/generate`.
  4. Heurísticas de segurança: detecção de "prompt echo" (quando o modelo devolve o próprio prompt) e fallbacks estáticos.

Principais variáveis de ambiente
- `MINDLY_TOKEN` — token Hugging Face Router (se usar HF).
- `API_KEYS` — chaves simples para autorização da API (cuidado em produção).
- `GEN_MODEL_MODE` — `hf` (padrão) para Hugging Face ou `local` para Ollama.
- `GEN_MODEL_NAME` — slug do modelo (HF) ou nome do modelo no Ollama.
- `EMOTION_MODEL` — modelo usado para detecção de emoções (HF).
- `OLLAMA_HOST`, `OLLAMA_PORT` — endereço do serviço Ollama (use `host.docker.internal` no Windows quando o Ollama roda no host).
- `GEN_TEMPERATURE`, `GEN_MAX_TOKENS` — parâmetros de geração.

Exemplos de chamadas

Detect (JSON -> retorna tópicos/alertas):

```powershell
curl -X POST http://localhost:8000/detect -H "Content-Type: application/json" -d '{"text":"Estou me sentindo muito triste ultimamente"}'
```

Analyze (requer `api-key` header configurado em `API_KEYS`):

```powershell
curl -X POST http://localhost:8000/analyze -H "Content-Type: application/json" -H "api-key: admin" -d '{"text":"Estou me sentindo muito triste ultimamente"}'
```

Segurança e boas práticas
- Nunca comite o `MINDLY_TOKEN` ou outros segredos no repositório.
- Em produção, substitua `API_KEYS` simples por um mecanismo de autenticação/autorizaçao robusto.
- Considere usar Docker Secrets, um cofre de segredos (Vault, AWS Secrets Manager, etc.) ou variáveis de ambiente do orquestrador.

Problemas comuns e soluções rápidas
- Erro relacionado a token do Hugging Face: verifique `MINDLY_TOKEN` no `.env`.
- Conexão com Ollama falha em Windows: ajuste `OLLAMA_HOST=host.docker.internal` e verifique firewall/local network.
- Para logs de debug, ajuste o nível de logging em `main.py` ou rode `docker compose logs -f mindly`.

Contribuindo / próximos passos
- Adicionar `docker-compose.override.yml` para desenvolvimento (montar volumes e hot-reload).
- Adicionar testes automatizados para endpoints e algumas validações de segurança.
- Integrar Docker Secrets para produção.

Se quiser, eu posso:
- alterar o `docker-compose` para também subir um container do `ollama` (atualmente o compose assume um Ollama externo/host);
- criar um `docker-compose.override.yml` para desenvolvimento;
- adicionar exemplos de testes (pytest) e/ou CI.

Licença
- Este repositório não inclui licença explícita. Se desejar, posso adicionar uma (MIT/Apache-2.0/etc.).

---
Arquivo alterado automaticamente para clarificar instalação e uso.

