
# Tech Challenge - Fase 1: API de Consulta de Livros

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://tech-challenge-livros.onrender.com)

## 1. Descrição do Projeto

Este projeto é a resposta ao Tech Challenge da Fase 1 do curso de Machine Learning Engineering. O objetivo principal é construir um pipeline de dados completo, desde a extração (scraping) até a disponibilização via uma API RESTful pública.

A aplicação coleta dados do site "Books to Scrape", processa essas informações e as armazena em um arquivo CSV. Em seguida, uma API desenvolvida com FastAPI lê esses dados e os expõe através de endpoints públicos para que possam ser consumidos por cientistas de dados, serviços de recomendação ou qualquer aplicação futura.

## 2. Plano Arquitetural

Esta seção detalha a arquitetura do projeto, cobrindo o pipeline de dados, planos de escalabilidade e integração com futuros modelos de Machine Learning.

### Pipeline de Dados: Ingestão → Processamento → API → Consumo

O fluxo de dados do projeto segue 4 etapas claras:

1.  **Fonte Externa:** `books.toscrape.com`
    * ⬇️
2.  **Ingestão (Scraper Python):** `scripts/scraper.py` (com Requests + BeautifulSoup)
    * ⬇️
3.  **Processamento/Carga (Armazenamento):** `data/books.csv` (formato estruturado)
    * ⬇️
4.  **Serviço (API):** `api/main.py` (FastAPI + Pandas)
    * ⬇️
5.  **Consumo (Cliente):** Cientista de Dados / Aplicação Web / Outros Serviços

* **Explicação do Fluxo:**
    * **1-2. Ingestão:** O script `scraper.py` acessa a fonte externa e extrai os dados brutos.
    * **2-3. Processamento/Carga:** O mesmo script limpa, formata e salva os dados no arquivo `data/books.csv`.
    * **3-4. Serviço:** A API FastAPI lê o arquivo CSV e o carrega na memória com Pandas para poder servir os dados.
    * **4-5. Consumo:** O cliente final (um Cientista de Dados) acessa os dados através dos endpoints públicos da API (ex: `GET /api/v1/books`).

### Arquitetura Pensada para Escalabilidade Futura

A arquitetura atual (CSV na memória) é ideal para prototipagem, mas não para produção em larga escala. O plano de escalabilidade envolve duas frentes:

1.  **Backend da API:** Desacoplar a API do arquivo CSV.
    * **Ação:** Substituir o `data/books.csv` por um **banco de dados real** (Ex: PostgreSQL ou MongoDB).
    * **Benefício:** A API não precisará carregar 1 milhão de livros na memória ao iniciar. Ela fará queries otimizadas (`SELECT * FROM books WHERE ...`) diretamente no banco, permitindo escalar os dados de forma independente da aplicação.

2.  **Pipeline de Ingestão:** Automatizar e robustecer o scraper.
    * **Ação:** Mover o `scraper.py` para um serviço de agendamento (como um **Cron Job**, **Celery Beat** ou uma **DAG no Airflow**).
    * **Benefício:** O scraping pode rodar automaticamente (ex: toda noite) e salvar os dados atualizados diretamente no banco de dados (criado na etapa anterior), mantendo a base de dados fresca sem intervenção manual.

### Cenário de Uso para Cientistas de Dados/ML

O objetivo principal desta API é servir como a fonte de dados "limpa" para a equipe de ciência de dados, conforme o desafio original.

* **Análise Exploratória (EDA):** Um Cientista de Dados pode consumir o endpoint `GET /api/v1/books` diretamente no Python para carregar todos os dados em um DataFrame Pandas e iniciar sua análise:
    ```python
    import pandas as pd
    url = "https://tech-challenge-livros.onrender.com/api/v1/books"
    df_livros = pd.read_json(url)
    print(df_livros.describe())
    print(df_livros['category'].value_counts())
    ```
* **Feature Engineering:** Os dados de `price`, `rating`, `availability` e `category` servem como features (variáveis) de entrada para treinar modelos de recomendação ou previsão de preço.

### Plano de Integração com Modelos de ML

Esta API é a **Fase 1** (servir dados de treino). O plano de integração com ML é a **Fase 2**:

1.  **Treinamento:** O Cientista de Dados usa a API (`GET /api/v1/books`) para obter os dados e treinar um modelo de recomendação (ex: filtro colaborativo ou baseado em conteúdo). O modelo treinado é salvo (ex: `model.pkl`).
2.  **Implantação (Deploy):** O modelo treinado é carregado na API (ou em um microserviço separado de inferência).
3.  **Criação de Endpoint de Previsão:** Um novo endpoint (como `POST /api/v1/recommendations`) seria criado na API.
4.  **Consumo do Modelo:**
    * Um aplicativo enviaria o ID de um livro ou um perfil de usuário para este novo endpoint.
    * A API, então, usaria o modelo carregado para **prever** e **retornar** uma lista de livros recomendados (cumprindo os requisitos bônus de ML-Ready).

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
A API agora está rodando localmente. Você pode acessar:

Documentação Swagger (Swagger UI): http://127.0.0.1:8000/docs

5. Documentação da API (Endpoints)
Abaixo estão os endpoints obrigatórios implementados. Todos os endpoints estão disponíveis na URL base: https://tech-challenge-livros.onrender.com

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
    "availability": 20,
    "category": "Historical Fiction",
    "image_url": "[https://books.toscrape.com/media/cache/26/0c/260c6ae16bce31c8f8c95daddd9f4a1c.jpg](https://books.toscrape.com/media/cache/26/0c/260c6ae16bce31c8f8c95daddd9f4a1c.jpg)",
    "book_url": "[https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html](https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html)"
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
GET /api/v1/books/search
Busca livros por título e/ou categoria. Os parâmetros são opcionais e case-insensitive.

Exemplo de Chamada (por Título): .../api/v1/books/search?title=Light

Exemplo de Chamada (por Categoria): .../A/api/v1/books/search?category=Poetry

Exemplo de Chamada (Combinada): .../api/v1/books/search?title=Light&category=Poetry

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
  }
]
GET /api/v1/categories
Lista todas as categorias de livros disponíveis.

Exemplo de Resposta (Sucesso 200):

JSON

{
  "categories": [
    "Poetry",
    "Historical Fiction",
    "History",
    "Philosophy",
    "Music",
    "Food and Drink"
  ],
  "total": 50
}
6. Links Finais
Link do Deploy (Render): https://tech-challenge-livros.onrender.com

Link da Documentação (Swagger): https://tech-challenge-livros.onrender.com/docs

Link do Vídeo (Apresentação): [COLE AQUI O LINK DO SEU VÍDEO NO YOUTUBE/LOOM]