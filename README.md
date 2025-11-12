# Mindly (mini ambiente)

Arquivos adicionados neste repositório para rodar a API Mindly localmente e um serviço Ollama em Docker.

Arquivos criados:
- `.env.example` — modelo de variáveis de ambiente (NÃO COMITAR com tokens reais).
- `requirements.txt` — dependências Python.
- `Dockerfile` — imagem para rodar a aplicação FastAPI.
- `docker-compose.yml` — orquestra `ollama` (ghcr.io/ollama/ollama) e o serviço `mindly`.
- `.dockerignore` — evita enviar arquivos indesejados para a build.

Importante: não commite credenciais. O seu token do Hugging Face é sensível e não deve aparecer no repositório.

Configurar localmente
1. Copie `.env.example` para `.env` e preencha a variável `MINDLY_TOKEN` com o seu token do Hugging Face.
   - Exemplo (não cole o token no repo):
     MINDLY_TOKEN=hf_seu_token_aqui
   - Se você preferir usar um nome/arquivo de segredo chamado `mindly-token`, mantenha esse arquivo *fora* do repositório.

2. Rodando com Docker Compose (recomendado):

   No PowerShell (Windows):

   ```powershell
   # Subir os containers em background
   docker compose up -d

   # Verificar logs (opcional)
   docker compose logs -f mindly
   ```

   O serviço `ollama` ficará escutando na porta 11434 e o `mindly` ficará na porta 8000.

3. Acessar a API:
   - Health: http://localhost:8000/health
   - Endpoints: POST http://localhost:8000/detect e POST http://localhost:8000/analyze

Notas e opções avançadas
- O `docker-compose.yml` usa a imagem `ghcr.io/ollama/ollama:latest`. Se você quiser uma versão específica ou um setup diferente (GPU, modelos locais, etc.) me diga que adapto o compose.
- Se preferir não executar o Ollama via Docker, você pode apontar `OLLAMA_HOST` para um serviço já existente (o `main.py` usa `OLLAMA_HOST` com default `ollama`).
- Para usar Docker Secrets/Swarm ou um gerenciador de segredos (recomendado em produção), me diga se quer que eu altere o compose para usar secrets.

Segurança
- Nunca coloque o token real no Git. Use `.env` local ou gerenciador de segredos.

Próximos passos sugeridos
- (Opcional) Adicionar suporte a Docker Secrets para não usar `.env` em produção.
- (Opcional) Adicionar um arquivo `docker-compose.override.yml` para desenvolvimento (montar volumes, reload automático).

