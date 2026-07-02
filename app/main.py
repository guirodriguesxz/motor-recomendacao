from fastapi import FastAPI, HTTPException, status
from app.schemas import HistoricoCompras, RecomendacaoResposta
from app.recomendador import EngineRecomendacao

app = FastAPI(
    title="API de Recomendação de Produtos",
    description="Microsserviço de Machine Learning para sugerir produtos.",
    version="1.0.0",
    docs_url="/api/v1/docs"
)

# Instancia a Engine
engine_ia = EngineRecomendacao()

@app.get("/health", status_code=status.HTTP_200_OK, tags=["Monitoramento"])
def verificar_saude():
    return {"status": "online"}

@app.post("/api/v1/recomendar", response_model=RecomendacaoResposta, tags=["Core ML"])
def processar_recomendacoes(payload: HistoricoCompras):
    try:
        sugestoes = engine_ia.gerar_sugestoes(
            produtos_comprados=payload.produtos_comprados, 
            top_n=3
        )
        metodo = "Similaridade de Cosseno" if payload.produtos_comprados else "Popularidade (Fallback)"
        
        return RecomendacaoResposta(
            cliente_id=payload.cliente_id,
            produtos_recomendados=sugestoes,
            metodo_utilizado=metodo
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
