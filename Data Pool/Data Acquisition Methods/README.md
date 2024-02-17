# Data Acquisition Methods

## Method 1: API Calls

### Step 1: Registration and Installation

1. Create an account here: [https://www.ncbi.nlm.nih.gov/myncbi/](https://www.ncbi.nlm.nih.gov/myncbi/)
2. Note the API key specified here: [https://account.ncbi.nlm.nih.gov/settings/](https://account.ncbi.nlm.nih.gov/settings/)
3. Install Entrez:
   `pip install entrezpy`

### Step 2: Execute Data_Acquisition.py

1. As this method is limited to fetch 9,998 records at a time we can split the fetch start and end date to accumulate them.

### Some Findings in this Method

1. This method of data acquisition is limited to fetch 9,998 records.
2. In-order to fasten the fetching process Data_Acquisition_Parallel_Threading utilised Process parallelization method. However, utilizing this method sometime results in blocking the API key by PubMed.

## Method 2: EDirect fetch

### Step 1: Installation

1. Installation commands:
   `sh -c "$(curl -fsSL https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh)"`
   `sh -c "$(wget -q https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh -O -)"`
2. Exporting the environment variables:
   `export PATH=${HOME}/edirect:${PATH}`
3. Setting the API key in bash_profile and .zshrc configuration files:
   `export NCBI_API_KEY=unique_api_key`

### Step 2: Execute Data_Acquisition.sh

### Some Findings in this Method

1. This method of data acquisition has no limit in record fetches.
2. This method is, time-consuming when compared to API calls method.

---

> Note: We have opted to gather the data utilizing the API calls method for our project.
> The deicision is based on the time taken to gather the data.
