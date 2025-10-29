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



@app.get("/api/v1/books/top-rated", tags=["Livros"])
async def get_top_rated_books():
    """
    Lista os livros com a melhor avaliação (rating mais alto).
    """
    check_data_loaded()
    
    # Encontra qual é a maior avaliação (ex: 5)
    max_rating = df_books['rating'].max()
    
    # Filtra o DataFrame
    top_rated_df = df_books[df_books['rating'] == max_rating]
    
    return dataframe_to_json(top_rated_df)


@app.get("/api/v1/books/price-range", tags=["Livros"])
async def get_books_by_price_range(
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
):
    """
    Filtra livros dentro de uma faixa de preço específica (min e/ou max).
    """
    check_data_loaded()
    
    result_df = df_books.copy()
    
    if min_price is not None:
        result_df = result_df[result_df['price'] >= min_price]
        
    if max_price is not None:
        result_df = result_df[result_df['price'] <= max_price]

    if result_df.empty:
        return {"message": "Nenhum livro encontrado nessa faixa de preço."}
        
    return dataframe_to_json(result_df)



@app.get("/api/v1/books/{book_id}", tags=["Livros"])
async def get_book_by_id(book_id: int):
    """
    Retorna detalhes completos de um livro específico pelo ID.
    (Este endpoint DEVE vir depois dos outros '/books/...')
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


@app.get("/api/v1/stats/overview", tags=["Stats"])
async def get_stats_overview():
    """
    Retorna estatísticas gerais da coleção: total de livros, preço médio e distribuição de ratings.
    """
    check_data_loaded()
    
    total_livros = len(df_books)
    preco_medio = round(df_books['price'].mean(), 2)
    
    # Conta a ocorrência de cada rating (ex: {5: 200, 4: 150, ...})
    # Converte o 'rating' (int64) para string para ser uma chave JSON válida
    distribuicao_ratings = df_books['rating'].value_counts().reset_index()
    distribuicao_ratings.columns = ['rating', 'count']
    distribuicao_ratings_dict = {str(row['rating']): row['count'] for index, row in distribuicao_ratings.iterrows()}

    
    return {
        "total_livros": total_livros,
        "preco_medio_geral": preco_medio,
        "distribuicao_ratings": distribuicao_ratings_dict
    }


@app.get("/api/v1/stats/categories", tags=["Stats"])
async def get_stats_by_category():
    """
    Retorna estatísticas detalhadas por categoria: contagem de livros, preço médio, min e max.
    """
    check_data_loaded()
    
    # Agrupa por categoria e calcula as estatísticas
    stats = df_books.groupby('category').agg(
        total_livros=('title', 'count'),
        preco_medio=('price', 'mean'),
        preco_min=('price', 'min'),
        preco_max=('price', 'max')
    ).reset_index() # Transforma o índice 'category' em coluna
    
    # Arredonda o preço médio
    stats['preco_medio'] = stats['preco_medio'].round(2)
    
    # Converte o DataFrame de estatísticas para JSON
    return stats.to_dict('records')



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)