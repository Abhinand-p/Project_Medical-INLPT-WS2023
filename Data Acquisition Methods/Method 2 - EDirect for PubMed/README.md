# Data Acquisition by performing EDirect fetch calls
This directory contains the code that can be utilised to fetch the PedMed data using EDirect

## Installation Guidelines
1. Installation commands:
   ``` sh -c "$(curl -fsSL https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh)" ```
   ``` sh -c "$(wget -q https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh -O -)" ```

2. Exporting the environment variables"
    ```   export PATH=${HOME}/edirect:${PATH} ```
3. Setting the API key in bash_profile and .zshrc configuration files:
    ``` export NCBI_API_KEY=unique_api_key ```

## Findings
1. This method of data acquisition is better than API calls as there is no limit in record fetches.

## Example 
esearch -db pubmed -query "intelligence[Title/Abstract] AND 2013/01/01:2014/12/31[Date - Publication]" | \
efetch -format xml -mode xml | \