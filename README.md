# MindlyAI — API de Análise Emocional e Risco

MindlyAI é uma API desenvolvida em FastAPI para análise rápida de textos, com foco em saúde mental, acolhimento e detecção de riscos. Ela identifica alertas, extrai tópicos, detecta emoções e gera respostas empáticas ou estruturadas, utilizando modelos de linguagem avançados (Groq, Hugging Face, etc.).

## Por que usar o MindlyAI?
- Automatize triagens e acolhimento em plataformas de saúde mental, chatbots, apps de suporte ou pesquisas.
- Detecte rapidamente sinais de risco (ideação suicida, depressão, ansiedade, etc.) em textos livres.
- Ofereça respostas empáticas e orientações seguras, reduzindo o tempo de resposta humana.
- Integre facilmente com qualquer sistema via HTTP/JSON.

## Endpoints disponíveis

### `/health` (GET)
Verifica se a API está online e saudável.
**Resposta:** `{ "status": "Saudavel" }`

### `/detect` (POST)
Recebe um texto e retorna:
- Se há palavras de alerta (ex: suicídio, depressão)
- Tópicos detectados (ex: trabalho, sono, alimentação)
- Pontuação de risco básica
**Exemplo de request:**
```json
{
  "text": "Estou me sentindo muito triste ultimamente"
}
```
**Exemplo de resposta:**
```json
{
  "alert": true,
  "alert_words": ["triste"],
  "topics": ["emoção"],
  "risk_score": 6
}
```

### `/speak` (POST)
Recebe um texto e (opcionalmente) metadados, e retorna uma resposta empática ou estruturada, gerada por IA.
- Pode ser usada para acolhimento, orientação ou triagem.
- Requer header `api-key` (veja `.env`)
**Exemplo de request:**
```json
{
  "text": "Não vejo mais sentido na vida",
  "meta": { "response_mode": "empathetic" }
}
```
**Exemplo de resposta:**
```json
{
  "generated": "Sinto muito que esteja passando por isso. Você não está sozinho..."
}
```

## Como usar o MindlyAI (passo a passo)

### 1. Pré-requisitos
- [Docker](https://www.docker.com/get-started) e [Docker Compose](https://docs.docker.com/compose/install/) instalados
- Ou: Python 3.11+ instalado (para rodar localmente)

### 2. Clone o repositório
```powershell
git clone <repo-url>
cd MindlyAI
```

### 3. Configure o ambiente
- Copie o arquivo de exemplo `.env.example` para `.env`:
```powershell
copy .env.example .env
```
- Edite `.env` e preencha:
  - `API_KEYS` (chave de acesso à API)
  - `GROQ_API_KEY` (obtenha em https://groq.com/)
  - Outros campos conforme desejado

### 4. Execute com Docker (recomendado)
```powershell
docker compose up --build
```
Acesse a documentação interativa em: [http://localhost:8000/docs](http://localhost:8000/docs)

## Exemplos de uso

### Detect
```powershell
curl -X POST http://localhost:8000/detect -H "Content-Type: application/json" -d '{"text":"Estou me sentindo muito triste ultimamente"}'
```

### Speak
```powershell
curl -X POST http://localhost:8000/speak -H "Content-Type: application/json" -H "api-key: admin" -d '{"text":"Estou me sentindo muito triste ultimamente"}'
```

## Variáveis de ambiente principais
- `API_KEYS`: chaves de acesso à API (separadas por vírgula)
- `GROQ_API_KEY`: chave de acesso ao Groq (obrigatória para geração)
- `GEN_MODEL_MODE`: "hf" (Hugging Face). Atualmente só Groq está ativo
- `GEN_MODEL_NAME`: nome/slug do modelo
- `GEN_TEMPERATURE`, `GEN_MAX_TOKENS`: parâmetros de geração

## Segurança e boas práticas
- Nunca comite segredos (tokens) no repositório.
- Em produção, use mecanismos robustos de autenticação/autorização.
- Considere usar Docker Secrets, Vault, AWS Secrets Manager, etc.

## Contribuindo
- Sugestões, issues e PRs são bem-vindos!
- Próximos passos: testes automatizados, CI, integração com Vault, exemplos de deploy.

## Licença
Este projeto não possui licença explícita. Se desejar, solicite a inclusão de uma licença (MIT, Apache-2.0, etc.).