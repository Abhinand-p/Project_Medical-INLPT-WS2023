# The code downloads all records in parallel that have the word intelligence in Title/Abstract between the years 2013
# to present.
# The code can still only gather the data from the first 9998 records.

# My API Key details
# Email: abhinand.po@gmail.com
# API Key: 542e3e9edc8dd6d9272f11dcda6d1e470309
from concurrent.futures import ThreadPoolExecutor
from Bio import Entrez

Entrez.email = 'abhinand.po@gmail.com'


def fetch_batch(api_key, search_query, retstart, retmax):
    Entrez.api_key = api_key
    handle = Entrez.esearch(db="pubmed", term=search_query, retmax=retmax, retstart=retstart)
    record = Entrez.read(handle)
    handle.close()

    batch_ids = record["IdList"]

    batch_articles = []
    for id in batch_ids:
        handle = Entrez.efetch(db="pubmed", id=id, rettype="medline", retmode="text")
        article_data = handle.read()
        batch_articles.append(article_data)
        handle.close()

    return batch_articles


def fetch_pubmed_data(api_key, search_term, start_year, retmax=100, batch_size=1000):
    # Fetch Query
    search_query = f'{search_term} [Title/Abstract] AND {start_year}/01/01[PDat]:3000/12/31[PDat]'

    # Total number of records
    handle = Entrez.esearch(db="pubmed", term=search_query, retmax=1)
    record = Entrez.read(handle)
    total_records = int(record["Count"])
    handle.close()

    # Fetch in batches using a Parallel Threading process
    articles = []
    with ThreadPoolExecutor() as executor:
        for retstart in range(0, total_records, batch_size):
            batch_articles = executor.submit(fetch_batch, api_key, search_query, retstart, retmax).result()
            articles.extend(batch_articles)
            print(f"Fetched {len(articles)} out of {total_records} articles.")

    return articles


def save_articles_to_file(articles, output_filename):
    with open(output_filename, 'w', encoding='utf-8') as file:
        for i, article in enumerate(articles, start=1):
            file.write(f"Article {i}:\n{article}\n{'=' * 80}\n\n")


if __name__ == "__main__":
    api_key = "542e3e9edc8dd6d9272f11dcda6d1e470309"
    search_term = "intelligence"
    start_year = 2013
    output_filename = "all_articles_in_parallel.txt"

    articles = fetch_pubmed_data(api_key, search_term, start_year)

    save_articles_to_file(articles, output_filename)

    print(f"All {len(articles)} articles saved to {output_filename}.")
