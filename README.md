Entendido. Sem frescura.

A culpa é da formatação do chat. Vou te mandar o texto puro (o código-fonte) do README.md.

Sua Tarefa:

Copie TUDO que está dentro do bloco cinza abaixo (clique no ícone de "Copiar" no canto, se houver).

Abra seu arquivo README.md.

Apague TUDO o que está nele.

Cole o texto que você copiou.

Salve e envie para o GitHub (git add ., git commit -m "readme final", git push).

Plaintext

# Tech Challenge - Fase 1: API de Consulta de Livros

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://tech-challenge-livros.onrender.com)

## 1. Descrição do Projeto

Este projeto é a resposta ao Tech Challenge da Fase 1 do curso de Machine Learning Engineering. O objetivo principal é construir um pipeline de dados completo, desde a extração (scraping) até a disponibilização via uma API RESTful pública.

A aplicação coleta dados do site "Books to Scrape", processa essas informações e as armazena em um arquivo CSV. Em seguida, uma API desenvolvida com FastAPI lê esses dados e os expõe através de endpoints públicos para que possam ser consumidos por cientistas de dados, serviços de recomendação ou qualquer aplicação futura.

## 2. Diagrama de Arquitetura (Plano Arquitetural)

O pipeline de dados e a arquitetura da aplicação seguem um fluxo simples e escalável:

http://googleusercontent.com/image_generation_content/0



* **Ingestão:** O script `scripts/scraper.py` acessa o site `books.toscrape.com` e extrai os dados de todos os livros.
* **Processamento/Armazenamento:** Os dados são limpos, estruturados (título, preço, rating, etc.) e salvos localmente no arquivo `data/books.csv`.
* **API:** A API FastAPI (`api/main.py`) é inicializada e carrega o CSV para a memória usando o Pandas. Ela é responsável por servir os dados.
* **Consumo:** A API é "deployada" publicamente no Render e pode ser consumida por cientistas de dados ou outras aplicações através de requisições HTTP.

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
git clone [https://github.com/WalterDeAlmeidaLira/TechChallenge.git](https://github.com/WalterDeAlmeidaLira/TechChallenge.git)
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