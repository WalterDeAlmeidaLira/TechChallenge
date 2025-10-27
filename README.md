Tech Challenge - Fase 1: API de Consulta de Livros
1. Descrição do Projeto
Este projeto é a resposta ao Tech Challenge da Fase 1 do curso de Machine Learning Engineering. O objetivo principal é construir um pipeline de dados completo, desde a extração (scraping) até a disponibilização via uma API RESTful pública.


A aplicação coleta dados do site "Books to Scrape" , processa essas informações e as armazena em um arquivo CSV. Em seguida, uma API desenvolvida com FastAPI lê esses dados e os expõe através de endpoints públicos para que possam ser consumidos por cientistas de dados, serviços de recomendação ou qualquer aplicação futura.





2. Diagrama de Arquitetura (Plano Arquitetural) 


O pipeline de dados e a arquitetura da aplicação seguem um fluxo simples e escalável:

+-------------------+      +------------------+      +---------------+      +-----------------+      +---------------+
|                   |      |                  |      |               |      |                 |      |               |
|  Books to Scrape  |----->|  Script (Scraper)  |----->|  data/books.csv |----->|  API (FastAPI)  |----->|  Cliente (Web/ |
|   (Fonte Externa) |      |  (scripts/scraper.py)|      |  (Armazenamento)  |      | (api/main.py)   |      |   Cientista)  |
|                   |      |                  |      |               |      |                 |      |               |
+-------------------+      +------------------+      +---------------+      +-----------------+      +---------------+
         |                        |                          |                      |                      |
     1. Extração              2. Transformação           3. Carga/Persistência       4. Serviço (API)         5. Consumo
   (Web Scraping)           (Limpeza, Estruturação)        (Arquivo Local)         (Endpoints RESTful)    (Requests HTTP)


Ingestão: O script scripts/scraper.py acessa o site books.toscrape.com e extrai os dados de todos os livros.


Processamento/Armazenamento : Os dados são limpos, estruturados (título, preço, rating, etc. ) e salvos localmente no arquivo data/books.csv.



API: A API FastAPI (api/main.py) é inicializada e carrega o CSV para a memória usando o Pandas. Ela é responsável por servir os dados.


Consumo : A API é "deployada" publicamente (ex: no Render) e pode ser consumida por cientistas de dados  ou outras aplicações através de requisições HTTP.


3. Tecnologias Utilizadas
Python 3.x


FastAPI : Para a construção da API RESTful e documentação Swagger automática.


Uvicorn: Para servir a aplicação FastAPI.

Pandas: Para manipulação e leitura eficiente do arquivo CSV.

Requests: Para fazer as requisições HTTP durante o scraping.

BeautifulSoup4: Para fazer o parsing do HTML do site.


Render: Para o deploy público da aplicação.

4. Instalação e Execução Local 


Siga os passos abaixo para executar o projeto em sua máquina local.

1. Clonar o Repositório:

Bash

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
4. Executar o Web Scraper: Este passo é necessário para gerar o arquivo data/books.csv.

Bash

python scripts/scraper.py
5. Executar a API Localmente:

Bash

uvicorn api.main:app --reload --port 8000
A API agora está rodando localmente. Você pode acessar:

API em execução: http://127.0.0.1:8000


Documentação Swagger (Swagger UI): http://127.0.0.1:8000/docs 

5. Documentação da API (Endpoints) 

Abaixo estão os endpoints obrigatórios implementados.


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
    "image_url": "https://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg",
    "book_url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
  },
  {
    "id": 2,
    "title": "Tipping the Velvet",
    "price": 53.74,
    ...
  }
]

GET /api/v1/books/{id} 

Retorna os detalhes completos de um livro específico pelo seu ID.

Exemplo de Chamada: GET /api/v1/books/1

Exemplo de Resposta (Sucesso 200):

JSON

{
  "id": 1,
  "title": "A Light in the Attic",
  "price": 51.77,
  "rating": 3,
  "availability": 22,
  "category": "Poetry",
  "image_url": "https://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg",
  "book_url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
}
Exemplo de Resposta (Erro 404):

JSON

{
  "detail": "Livro com ID 9999 não encontrado."
}

GET /api/v1/books/search 

Busca livros por título e/ou categoria. Os parâmetros são opcionais e case-insensitive.

Exemplo de Chamada (por Título): GET /api/v1/books/search?title=Light

Exemplo de Chamada (por Categoria): GET /api/v1/books/search?category=Poetry

Exemplo de Chamada (Combinada): GET /api/v1/books/search?title=Light&category=Poetry

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
    ...
  ],
  "total": 50
}
6. Links Finais

Link do Deploy (Render): [COLE AQUI A SUA URL PÚBLICA DO RENDER] 




Link do Vídeo (Apresentação): [COLE AQUI O LINK DO SEU VÍDEO NO YOUTUBE/LOOM]