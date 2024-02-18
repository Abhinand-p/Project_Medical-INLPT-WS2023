# The code downloads all records that have the word intelligence in Title/Abstract between the years 2013 to present.

# My API Key details
# Email: abhinand.po@gmail.com
# API Key: e8f5322b604f671d0ab3e9bd5a1933d7dc08
import csv
from Bio import Entrez


def fetch_pubmed_data(api_key, search_term, start_year, end_year, retmax=100):
    Entrez.email = "abhinand.po@gmail.com"
    Entrez.api_key = api_key

    # Fetch Query
    search_query = f'{search_term} [Title/Abstract] AND {start_year}/10/01[PDat]:{end_year}/12/31[PDat]'

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

        batch_articles = []
        for id in record["IdList"]:
            handle = Entrez.efetch(db="pubmed", id=id, rettype="medline", retmode="text")
            article_data = handle.read()
            batch_articles.append(article_data)
            handle.close()

        articles.extend(batch_articles)

        # Save batch to CSV
        save_articles_to_csv(batch_articles, "Articles_2023_4.csv")

        print(f"Fetched {len(articles)} out of {total_records} articles.")

    return articles


def save_articles_to_csv(articles, output_filename):
    with open(output_filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Article']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        for i, article in enumerate(articles, start=1):
            writer.writerow({'Article': article})

if __name__ == "__main__":
    api_key = "e8f5322b604f671d0ab3e9bd5a1933d7dc08"
    search_term = "intelligence"
    start_year = 2023
    end_year = 2023

    # Open the CSV file and write the header
    with open("Articles_2023_4.csv", 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Article']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    articles = fetch_pubmed_data(api_key, search_term, start_year, end_year)

    print(f"All {len(articles)} articles saved to the same CSV file (all_articles.csv).")
