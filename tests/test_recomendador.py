from app.recomendador import EngineRecomendacao

engine = EngineRecomendacao()


def test_cliente_novo_recebe_populares():
    sugestoes = engine.gerar_sugestoes([], top_n=3)
    assert sugestoes == engine.produtos_populares[:3]


def test_nao_recomenda_produto_ja_comprado():
    comprados = ["Corte de Cabelo Masculino"]
    sugestoes = engine.gerar_sugestoes(comprados, top_n=3)
    assert "Corte de Cabelo Masculino" not in sugestoes


def test_respeita_top_n():
    sugestoes = engine.gerar_sugestoes(["Pomada Modeladora Ultra"], top_n=2)
    assert len(sugestoes) <= 2


def test_sem_similaridade_cai_no_fallback_de_populares():
    sugestoes = engine.gerar_sugestoes(["xyzabc"], top_n=3)
    assert sugestoes
    assert all(s in engine.produtos_populares for s in sugestoes)
