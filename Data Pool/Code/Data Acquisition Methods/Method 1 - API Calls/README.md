# Data Acquisition by performing API Calls
This directory contains the code that can be utilised to fetch the PedMed data using API calls

## Registration and Installation Guidelines
1. Create an account here: https://www.ncbi.nlm.nih.gov/myncbi/
2. Note the API key specified here: https://account.ncbi.nlm.nih.gov/settings/
3. Install Entrez: pip install entrezpy 

## Findings
1. This method of data acquisition is limited to fetch 9,998 records.
2. This method can be modified to be called by a shell script with different dates in-order to capture all the records(61,004).
3. In-order to fasten the fetching process Data_Acquisition_Parallel_Threading utilised Process parallelization method.
3. PubMed also offers EDirect method which can be utilised to fetch all records at once. This method development is ongoing.
