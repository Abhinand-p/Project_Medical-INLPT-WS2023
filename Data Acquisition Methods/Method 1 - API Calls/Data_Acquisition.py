# The code downloads all records that have the word intelligence in Title/Abstract between the years 2013 to present.

# My API Key details
# Email: abhinand.po@gmail.com
# API Key: 542e3e9edc8dd6d9272f11dcda6d1e470309
from Bio import Entrez


def fetch_pubmed_data(api_key, search_term, start_year, end_year, retmax=100):
    Entrez.email = "abhinand.po@gmail.com"
    Entrez.api_key = api_key

    # Fetch Query
    search_query = f'{search_term} [Title/Abstract] AND {start_year}/01/01[PDat]:{end_year}/12/31[PDat]'

    # Total number of records
    handle = Entrez.esearch(db="pubmed", term=search_query, retmax=retmax)
    record = Entrez.read(handle)
    total_records = int(record["Count"])
    handle.close()

    # Fetch in batches
    articles = []
    for retstart in range(0, total_records, retmax):
        handle = Entrez.esearch(db="pubmed", term=search_query, retmax=retmax, retstart=retstart)
        record = Entrez.read(handle)
        handle.close()

        for id in record["IdList"]:
            handle = Entrez.efetch(db="pubmed", id=id, rettype="medline", retmode="text")
            article_data = handle.read()
            articles.append(article_data)
            handle.close()

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
    end_year = 2014
    output_filename = "all_articles.txt"

    articles = fetch_pubmed_data(api_key, search_term, start_year, end_year)

    save_articles_to_file(articles, output_filename)

    print(f"All {len(articles)} articles saved to {output_filename}.")
