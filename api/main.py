import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import os
from typing import Optional

app = FastAPI(
    title="API de Consulta de Livros",
    description="API para consulta de dados extraídos do 'Books to Scrape'",
    version="1.0.0"
)

DATA_PATH = os.path.join("data", "books.csv")
df_books = None

def load_data():
    """Carrega os dados do CSV para um DataFrame pandas."""
    global df_books
    try:
        df_books = pd.read_csv(DATA_PATH, sep=';')
        print(f"Dados carregados com sucesso. Total de {len(df_books)} livros.")
    except FileNotFoundError:
        print(f"Erro: Arquivo {DATA_PATH} não encontrado.")
        df_books = pd.DataFrame()

@app.on_event("startup")
async def startup_event():
    load_data()

def check_data_loaded():
    """Verifica se os dados foram carregados."""
    if df_books is None or df_books.empty:
        raise HTTPException(status_code=503, detail="Serviço indisponível: os dados dos livros não puderam ser carregados.")

def dataframe_to_json(df):
    """Converte DataFrame para uma lista de dicionários (JSON)."""
    return df.to_dict('records')

@app.get("/api/v1/health", tags=["Status"])
async def get_health():
    """
    Verifica o status da API e a disponibilidade dos dados.
    """
    if df_books is None or df_books.empty:
        return JSONResponse(
            status_code=503,
            content={"status": "error", "message": "Dados dos livros não carregados."}
        )
    return {"status": "ok", "message": "API operacional e dados carregados."}


@app.get("/api/v1/books", tags=["Livros"])
async def get_all_books():
    """
    Lista todos os livros disponíveis na base de dados.
    """
    check_data_loaded()
    return dataframe_to_json(df_books)

@app.get("/api/v1/books/search", tags=["Livros"])
async def search_books(
    title: Optional[str] = None,
    category: Optional[str] = None
):
    """
    Busca livros por título e/ou categoria.
    Ambos os parâmetros são opcionais.
    """
    check_data_loaded()

    result_df = df_books.copy()

    if title:
        result_df = result_df[result_df['title'].str.contains(title, case=False, na=False)]

    if category:
        result_df = result_df[result_df['category'].str.lower() == category.lower()]

    if result_df.empty:
        return {"message": "Nenhum livro encontrado com os critérios fornecidos."}

    return dataframe_to_json(result_df)



@app.get("/api/v1/books/{book_id}", tags=["Livros"])
async def get_book_by_id(book_id: int):
    """
    Retorna detalhes completos de um livro específico pelo ID.
    """
    check_data_loaded()
    
    try:
        book = df_books[df_books['id'] == book_id]
        
        if book.empty:
            raise HTTPException(status_code=404, detail=f"Livro com ID {book_id} não encontrado.")
        
        return dataframe_to_json(book)[0]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao processar a solicitação: {e}")



@app.get("/api/v1/categories", tags=["Categorias"])
async def get_all_categories():
    """
    Lista todas as categorias de livros disponíveis.
    """
    check_data_loaded()
    
    categories = df_books['category'].unique().tolist()
    
    return {"categories": categories, "total": len(categories)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)