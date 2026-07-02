import pandas as pd
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List

class EngineRecomendacao:
    def __init__(self):
        # Caminho dinâmico para encontrar o CSV independentemente de onde o script rode
        caminho_csv = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'catalogo.csv')
        
        try:
            # Lendo os dados do CSV usando o Pandas
            df_catalogo = pd.read_csv(caminho_csv)
            self.catalogo_produtos = df_catalogo['produto'].tolist()
            
            # Pegando os 3 produtos mais populares dinamicamente para o fallback (Cold Start)
            df_populares = df_catalogo.sort_values(by='popularidade', ascending=False)
            self.produtos_populares = df_populares['produto'].head(3).tolist()
        except FileNotFoundError:
            print("⚠️ Arquivo catalogo.csv não encontrado. Usando dados em memória (Fallback).")
            self.catalogo_produtos = ["Corte de Cabelo Masculino", "Pomada Modeladora Ultra", "Óleo Essencial para Barba"]
            self.produtos_populares = self.catalogo_produtos[:3]

    def gerar_sugestoes(self, produtos_comprados: List[str], top_n: int = 3) -> List[str]:
        # Se o cliente não comprou nada, sugere os mais populares
        if not produtos_comprados:
            return self.produtos_populares[:top_n]

        # Junta tudo que o cliente comprou em um texto só
        texto_historico = " ".join(produtos_comprados)
        corpus = [texto_historico] + self.catalogo_produtos
        
        # Matemática: Transformando texto em números para achar a similaridade
        vetorizador = CountVectorizer()
        matriz_frequencia = vetorizador.fit_transform(corpus)
        
        matrizes_similaridade = cosine_similarity(matriz_frequencia[0:1], matriz_frequencia[1:])
        scores = matrizes_similaridade[0]
        
        # Criando uma tabela temporária para ordenar os que combinam mais
        resultados = pd.DataFrame({
            'produto': self.catalogo_produtos,
            'score': scores
        }).sort_values(by='score', ascending=False)
        
        # Filtrando o que ele já comprou
        recomendacoes_filtradas = []
        for _, linha in resultados.iterrows():
            if linha['produto'] not in produtos_comprados and linha['score'] > 0.0:
                recomendacoes_filtradas.append(linha['produto'])
        
        # Se nenhuma correlação matemática for encontrada, sugere populares
        if not recomendacoes_filtradas:
            recomendacoes_filtradas = [item for item in self.produtos_populares if item not in produtos_comprados]
                    
        return recomendacoes_filtradas[:top_n]