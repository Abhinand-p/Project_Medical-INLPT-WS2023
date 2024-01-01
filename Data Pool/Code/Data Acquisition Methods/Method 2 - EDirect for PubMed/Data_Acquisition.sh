#!/bin/bash

start_year=2013
end_year=2023
search_term="intelligence"

# Utilizing EDirect method to retrieve PubMed records
esearch -db pubmed -query "${search_term}[Title/Abstract] AND ${start_year}:${end_year}[PDAT]" | \
efetch -format pubmed > intelligence_articles.xml