# Motor de Recomendação de Produtos

[![CI](https://github.com/guirodriguesxz/motor-recomendacao/actions/workflows/ci.yml/badge.svg)](https://github.com/guirodriguesxz/motor-recomendacao/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)

Microsserviço em **Python + FastAPI** que recomenda produtos a partir do histórico de compras
de um cliente, usando **vetorização de texto e similaridade de cosseno** (scikit-learn).
Foi pensado para ser consumido via REST por um back-end principal (Spring Boot, Node.js etc.).

## Stack

- **FastAPI** + **Pydantic v2** — API e validação de payload
- **scikit-learn** (`CountVectorizer`, `cosine_similarity`) + **pandas**
- **pytest** + `TestClient` — testes unitários e de API
- **Docker** — imagem pronta para deploy
- **GitHub Actions** — testes e build da imagem a cada push/PR

## Como funciona

```
POST /api/v1/recomendar
        │
        ▼
 histórico vazio? ──sim──► mais populares (cold start)
        │ não
        ▼
 vetoriza histórico + catálogo (CountVectorizer)
        │
        ▼
 similaridade de cosseno histórico × cada produto
        │
        ▼
 ordena por score, remove itens já comprados e score 0
        │
        ▼
 nenhum match? ──sim──► mais populares (fallback)
        │ não
        ▼
     top N itens
```

O catálogo fica em [`catalogo.csv`](catalogo.csv) (produto, categoria, preço, popularidade).

## Como rodar

### Docker

```bash
docker build -t motor-recomendacao .
docker run -p 8000:8000 motor-recomendacao
```

### Local

```bash
git clone https://github.com/guirodriguesxz/motor-recomendacao.git
cd motor-recomendacao
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger: http://localhost:8000/api/v1/docs

## Exemplos de requisição

**Cliente com histórico**

```bash
curl -X POST http://localhost:8000/api/v1/recomendar \
  -H "Content-Type: application/json" \
  -d '{"cliente_id": 1024, "produtos_comprados": ["Corte de Cabelo Masculino"]}'
```

Resposta:

```json
{
  "cliente_id": 1024,
  "produtos_recomendados": ["...", "...", "..."],
  "metodo_utilizado": "Similaridade de Cosseno"
}
```

**Cliente novo (cold start)**

```bash
curl -X POST http://localhost:8000/api/v1/recomendar \
  -H "Content-Type: application/json" \
  -d '{"cliente_id": 7, "produtos_comprados": []}'
```

Resposta: os 3 itens com maior `popularidade` no catálogo e `"metodo_utilizado": "Popularidade (Fallback)"`.

**Health check**

```bash
curl http://localhost:8000/health
# {"status": "online"}
```

## Testes

```bash
pip install -r requirements-dev.txt
pytest -v
```

Cobrem: cold start, filtro de itens já comprados, limite `top_n`, fallback sem similaridade,
endpoints `/health` e `/api/v1/recomendar` e validação de payload (422).

## Próximos passos

- Trocar `CountVectorizer` por TF-IDF / embeddings e pré-computar a matriz do catálogo na inicialização
- Usar categoria e preço como features
- Persistir histórico em banco e expor métricas (Prometheus)
