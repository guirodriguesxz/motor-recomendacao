from pydantic import BaseModel, Field
from typing import List

class HistoricoCompras(BaseModel):
    cliente_id: int = Field(..., description="ID identificador único do cliente")
    produtos_comprados: List[str] = Field(..., description="Lista de produtos comprados anteriormente")

    model_config = {
        "json_schema_extra": {
            "example": {
                "cliente_id": 1024,
                "produtos_comprados": ["Corte de Cabelo Masculino", "Pomada Modeladora"]
            }
        }
    }

class RecomendacaoResposta(BaseModel):
    cliente_id: int
    produtos_recomendados: List[str]
    metodo_utilizado: str
