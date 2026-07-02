# Motor de Recomendação de Produtos (IA) 🚀

Este projeto é um microsserviço de Inteligência Artificial construído em Python com **FastAPI**. Ele atua como um motor de recomendação utilizando **Machine Learning (Similaridade de Cosseno)** para sugerir produtos relevantes com base no histórico de compras do usuário.

A arquitetura foi projetada para ser facilmente integrada via API RESTful a back-ends robustos (como Java/Spring Boot ou Node.js), simulando um ambiente corporativo real.

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python 3.9+
* **Framework Web:** FastAPI (Alta performance e assíncrono)
* **Machine Learning:** Scikit-Learn (CountVectorizer, Cosine Similarity)
* **Processamento de Dados:** Pandas
* **Servidor:** Uvicorn

## ⚙️ Como a Inteligência Artificial Funciona?
O motor lê o catálogo de produtos a partir de uma fonte de dados (`catalogo.csv`). Quando recebe um payload via `POST` com o histórico do usuário, ele:
1. Vetoriza o texto das compras anteriores.
2. Aplica a fórmula matemática de **Similaridade de Cosseno** para encontrar a distância vetorial entre o que o cliente comprou e o restante do catálogo.
3. Retorna os 3 itens com maior probabilidade de conversão.
4. Possui um sistema de *Fallback* (Cold Start) que sugere os itens mais populares caso o cliente seja novo.

## 🚀 Como rodar o projeto localmente

1. Clone o repositório e acesse a pasta do projeto:
```bash
git clone [https://github.com/SEU-USUARIO/motor-recomendacao.git](https://github.com/SEU-USUARIO/motor-recomendacao.git)
cd motor-recomendacao# motor-recomendacao
