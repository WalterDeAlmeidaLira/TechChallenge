# Tech Challenge - Fase 1: API de Consulta de Livros

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://tech-challenge-livros.onrender.com)

## 1. Descrição do Projeto

Este projeto é a resposta ao Tech Challenge da Fase 1 do curso de Machine Learning Engineering. O objetivo principal é construir um pipeline de dados completo, desde a extração (scraping) até a disponibilização via uma API RESTful pública.

A aplicação coleta dados do site "Books to Scrape", processa essas informações e as armazena em um arquivo CSV. Em seguida, uma API desenvolvida com FastAPI lê esses dados e os expõe através de endpoints públicos para que possam ser consumidos por cientistas de dados, serviços de recomendação ou qualquer aplicação futura.

## 2. Plano Arquitetural

Esta seção detalha a arquitetura do projeto, cobrindo o pipeline de dados, planos de escalabilidade e integração com futuros modelos de Machine Learning.

### Pipeline de Dados: Ingestão → Processamento → API → Consumo

link para o pdf com arquitetura:
![Diagrama de Arquitetura](data/diagrama.pdf) 

* **Explicação do Fluxo:**
    * **Ingestão:** O script `scripts/scraper.py` acessa a fonte externa (`books.toscrape.com`) e extrai os dados brutos.
    * **Processamento/Carga:** O mesmo script limpa, formata e salva os dados no arquivo `data/books.csv`.
    * **Serviço:** A API FastAPI (`api/main.py`) lê o arquivo CSV e o carrega na memória com Pandas para poder servir os dados.
    * **Consumo:** O cliente final (um Cientista de Dados) acessa os dados através dos endpoints públicos da API (ex: `GET /api/v1/books`).

### Arquitetura Pensada para Escalabilidade Futura

A arquitetura atual (CSV na memória) é ideal para prototipagem. O plano de escalabilidade envolve:

1.  **Backend da API:** Substituir o `data/books.csv` por um **banco de dados real** (Ex: PostgreSQL) para que a API não precise carregar tudo na memória e possa fazer queries otimizadas.
2.  **Pipeline de Ingestão:** Automatizar o `scraper.py` com um **agendador** (Ex: Airflow ou Cron Job) para atualizar o banco de dados periodicamente.

### Cenário de Uso para Cientistas de Dados/ML

O objetivo principal desta API é servir como a fonte de dados "limpa" para a equipe de ciência de dados.

* **Análise Exploratória (EDA):** Um Cientista de Dados pode consumir o endpoint `GET /api/v1/books` para carregar todos os dados em um DataFrame Pandas:
    ```python
    import pandas as pd
    url = "https://tech-challenge-livros.onrender.com/api/v1/books"
    df_livros = pd.read_json(url)
    print(df_livros.describe())
    ```
* **Feature Engineering:** Os dados de `price`, `rating`, `availability` e `category` servem como features de entrada para modelos.

### Plano de Integração com Modelos de ML

Esta API é a **Fase 1** (servir dados de treino). O plano de integração com ML é a **Fase 2**:

1.  **Treinamento:** O Cientista de Dados usa a API (`GET /api/v1/books`) para obter os dados e treinar um modelo de recomendação.
2.  **Implantação (Deploy):** O modelo treinado é carregado na API.
3.  **Criação de Endpoint de Previsão:** Um novo endpoint (como `POST /api/v1/recommendations`) seria criado para receber o ID de um livro e retornar uma lista de recomendações.

## 3. Tecnologias Utilizadas

* **Python 3.x**
* **FastAPI:** Para a construção da API RESTful e documentação Swagger automática.
* **Uvicorn:** Para servir a aplicação FastAPI.
* **Pandas:** Para manipulação e leitura eficiente do arquivo CSV.
* **Requests:** Para fazer as requisições HTTP during o scraping.
* **BeautifulSoup4:** Para fazer o parsing do HTML do site.
* **Render:** Para o deploy público da aplicação.

## 4. Instalação e Execução Local

Siga os passos abaixo para executar o projeto em sua máquina local.

**1. Clonar o Repositório:**
```bash
git clone https://github.com/WalterDeAlmeidaLira/TechChallenge.git
cd TechChallenge
2. Criar e Ativar o Ambiente Virtual:

Bash

# Criar o ambiente
python -m venv venv

# Ativar no Windows
.\venv\Scripts\activate

# Ativar no Mac/Linux
source venv/bin/activate
3. Instalar as Dependências:

Bash

pip install -r requirements.txt
4. Executar o Web Scraper: (Este passo é necessário para gerar o arquivo data/books.csv.)

Bash

python scripts/scraper.py
5. Executar a API Localmente:

Bash

uvicorn api.main:app --reload --port 8000
Documentação Swagger (Swagger UI): http://12s7.0.0.1:8000/docs

5. Documentação da API (Endpoints)
Abaixo estão todos os endpoints implementados. URL Base: https://tech-challenge-livros.onrender.com

Endpoints Obrigatórios
GET /api/v1/health
Verifica o status da API e a conectividade com os dados.

Exemplo de Resposta (Sucesso 200):

JSON

{
  "status": "ok",
  "message": "API operacional e dados carregados."
}
GET /api/v1/books
Lista todos os livros disponíveis na base de dados.

Exemplo de Resposta (Sucesso 200):

JSON

[
  {
    "id": 1,
    "title": "A Light in the Attic",
    "price": 51.77,
    "rating": 3,
    "availability": 22,
    "category": "Poetry",
    "image_url": "[https://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg](https://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg)",
    "book_url": "[https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html](https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html)"
  },
  {
    "id": 2,
    "title": "Tipping the Velvet",
    "price": 53.74,
    ...
  }
]
GET /api/v1/books/search
Busca livros por título e/ou categoria. Os parâmetros são opcionais e case-insensitive.

Exemplo de Chamada (por Título): .../api/v1/books/search?title=Light

Exemplo de Chamada (por Categoria): .../api/v1/books/search?category=Poetry

Exemplo de Resposta (Sucesso 200):

JSON

[
  {
    "id": 1,
    "title": "A Light in the Attic",
    "price": 51.77,
    ...
  }
]
GET /api/v1/books/{id}
Retorna os detalhes completos de um livro específico pelo seu ID.

Exemplo de Chamada: .../api/v1/books/1

Exemplo de Resposta (Sucesso 200):

JSON

{
  "id": 1,
  "title": "A Light in the Attic",
  "price": 51.77,
  "rating": 3,
  "availability": 22,
  "category": "Poetry",
  "image_url": "[https://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg](https://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg)",
  "book_url": "[https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html](https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html)"
}
Exemplo de Resposta (Erro 404):

JSON

{
  "detail": "Livro com ID 9999 não encontrado."
}
GET /api/v1/categories
Lista todas as categorias de livros disponíveis.

Exemplo de Resposta (Sucesso 200):

JSON

{
  "categories": [
    "Poetry",
    "Historical Fiction",
    "History",
    ...
  ],
  "total": 50
}
Endpoints Opcionais (Insights)
GET /api/v1/books/top-rated
Lista os livros com a melhor avaliação (rating mais alto, ex: 5 estrelas).

Exemplo de Chamada: .../api/v1/books/top-rated

Exemplo de Resposta (Sucesso 200):

JSON

[
  {
    "id": 3,
    "title": "Olio",
    "price": 23.88,
    "rating": 5,
    "availability": 19,
    "category": "Poetry",
    ...
  },
  {
    "id": 10,
    "title": "Sharp Objects",
    "price": 47.82,
    "rating": 5,
    ...
  }
]
GET /api/v1/books/price-range
Filtra livros dentro de uma faixa de preço específica ( min_price e/ou max_price).

Exemplo de Chamada: .../api/v1/books/price-range?min_price=55&max_price=60

Exemplo de Resposta (Sucesso 200):

JSON

[
  {
    "id": 20,
    "title": "The Four Agreements: A Practical Guide to Personal Freedom (A Toltec Wisdom Book)",
    "price": 57.25,
    "rating": 5,
    ...
  }
]
GET /api/v1/stats/overview
Retorna estatísticas gerais da coleção: total de livros, preço médio e distribuição de ratings.

Exemplo de Chamada: .../api/v1/stats/overview

Exemplo de Resposta (Sucesso 200):

JSON

{
  "total_livros": 1000,
  "preco_medio_geral": 35.07,
  "distribuicao_ratings": {
    "3": 203,
    "1": 200,
    "5": 199,
    "2": 199,
    "4": 199
  }
}
GET /api/v1/stats/categories
Retorna estatísticas detalhadas por categoria (contagem de livros, preço médio, min e max).

Exemplo de Chamada: .../api/v1/stats/categories

Exemplo de Resposta (Sucesso 200):

JSON

[
  {
    "category": "Add a comment",
    "total_livros": 67,
    "preco_medio": 35.85,
    "preco_min": 10.02,
    "preco_max": 59.98
  },
  {
    "category": "Art",
    "total_livros": 8,
    "preco_medio": 43.14,
    "preco_min": 21.98,
    "preco_max": 58.09
  },
  ...
]
6. Links Finais
Link do Deploy (Render): https://tech-challenge-livros.onrender.com

Link da Documentação (Swagger): https://tech-challenge-livros.onrender.com/docs

Link do Vídeo (Apresentação):