# Sistema de Automação de Leads (FastAPI)

Projeto esqueleto para receber, processar e qualificar leads via API, com integração simples para n8n/Traefik.

## Tecnologias
- Python 3.10+
- FastAPI
- SQLAlchemy (Sync)
- PostgreSQL
- Uvicorn
- Docker / docker-compose
- Traefik (exemplo de labels no docker-compose)

## Como usar (modo rápido - sem Docker)
1. Crie um ambiente virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Ajuste `app/config.py` com as credenciais do banco (ou use variáveis de ambiente).
3. Crie o banco PostgreSQL e execute `data/sample_data.sql` para criar a tabela:
   ```bash
   psql -U postgres -d automacao_leads -f data/sample_data.sql
   ```
4. Rode a aplicação:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
5. Acesse a documentação interativa em `http://localhost:8000/docs`.

## Com Docker (exemplo)
- Ajuste variáveis no `docker-compose.yml` (senhas) e rode:
  ```bash
  docker-compose up --build
  ```

## Endpoints principais
- `POST /leads` — criar lead e aplicar scoring automático.
- `GET /leads` — listar leads (filtros por status, origem).
- `GET /leads/{id}` — obter detalhes.
- `PUT /leads/{id}` — atualizar lead/classificação.

## Integração com n8n
- Aponte um Webhook do n8n para `http://your-host/api/webhook/n8n` (exemplo fornecido).
- O endpoint aceitará payloads e os armazenará no banco.

Desenvolvido para ser facilmente adaptado e estendido.

# Como rodar no Portainer
Entre no Portainer → Stacks → Add Stack.

Nome da Stack: automacao-leads.

Selecione a opção "Repository".

## Repository URL:

https://github.com/brunopirz/automacao-leads

## Repository reference:
main

Compose path:
docker-compose.yml

Deploy the Stack.

O que vai acontecer
O Portainer fará git clone direto do seu repositório.

Usará o Dockerfile do projeto para buildar a imagem do app já com todo o código.

Subirá o PostgreSQL e o Traefik juntos.

O Traefik vai expor sua API no domínio api.seudominio.com com HTTPS automático (precisa apontar DNS para a VPS).

## 📌 Observações importantes:

#### Substitua seu-email@dominio.com pelo email que quer usar no Let's Encrypt.

#### Substitua api.seudominio.com pelo domínio real.

Certifique-se de que o DNS do domínio aponta para o IP da VPS onde o Portainer está rodando.
