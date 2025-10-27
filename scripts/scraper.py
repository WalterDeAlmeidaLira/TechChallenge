import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os

BASE_URL = "https://books.toscrape.com/"
CATALOGUE_URL = BASE_URL + "catalogue/" 
DATA_DIR = "data"
CSV_FILE = os.path.join(DATA_DIR, "books.csv")

RATING_MAP = {
    'One': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5
}

def get_soup(url):
    """Faz a requisição e retorna um objeto BeautifulSoup."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.RequestException as e:
        print(f"Erro ao acessar a URL {url}: {e}")
        return None

def parse_book_details(book_url):
    """Extrai detalhes de uma página de livro específica."""
    soup = get_soup(book_url)
    if not soup:
        return None

    try:
        category = soup.find('ul', class_='breadcrumb').find_all('li')[2].a.text
        
        image_relative_url = soup.find('div', class_='item active').img['src']
        image_url = BASE_URL + image_relative_url.replace('../', '') 

        availability_text = soup.find('p', class_='instock availability').text.strip()
        availability = int(re.search(r'\d+', availability_text).group())

        return category, image_url, availability
    
    except Exception as e:
        print(f"Erro ao parsear detalhes do livro {book_url}: {e}")
        return None

def scrape_books():
    """Função principal para varrer o site e extrair os dados."""
    print("Iniciando o processo de scraping...")
    all_books_data = []
    current_url = CATALOGUE_URL + "page-1.html"
    page_count = 1

    while current_url:
        print(f"Scraping página: {page_count}...")
        soup = get_soup(current_url)
        if not soup:
            break

        books_on_page = soup.find_all('article', class_='product_pod')

        for book in books_on_page:
            try:
                # 1. Título
                title = book.h3.a['title']
                
                # 2. Preço
                price = float(book.find('p', class_='price_color').text.replace('£', '').replace('Â', ''))
                
                # 3. Rating
                rating_text = book.find('p', class_='star-rating')['class'][1]
                rating = RATING_MAP.get(rating_text, 0)
                
                book_relative_url = book.h3.a['href']
                book_url = CATALOGUE_URL + book_relative_url
                
                # 4, 5, 6. Categoria, Imagem, Disponibilidade
                details = parse_book_details(book_url)
                if details:
                    category, image_url, availability = details
                else:
                    print(f"Não foi possível obter detalhes do livro: {title}")
                    continue

                all_books_data.append({
                    'title': title,
                    'price': price,
                    'rating': rating,
                    'availability': availability,
                    'category': category,
                    'image_url': image_url,
                    'book_url': book_url
                })

            except Exception as e:
                print(f"Erro ao processar um livro: {e}")

        next_page_tag = soup.find('li', class_='next')
        if next_page_tag:
            next_page_url = next_page_tag.a['href']
            current_url = CATALOGUE_URL + next_page_url
            page_count += 1
        else:
            current_url = None

    print(f"Scraping finalizado. Total de {len(all_books_data)} livros encontrados.")
    return all_books_data

def save_to_csv(data):
    """Salva os dados extraídos em um arquivo CSV."""
    if not data:
        print("Nenhum dado para salvar.")
        return

    os.makedirs(DATA_DIR, exist_ok=True)
    
    df = pd.DataFrame(data)
    
    df.insert(0, 'id', range(1, len(df) + 1))
    
    df.to_csv(CSV_FILE, index=False, encoding='utf-8',sep=';')

if __name__ == "__main__":
    books_data = scrape_books()
    save_to_csv(books_data)