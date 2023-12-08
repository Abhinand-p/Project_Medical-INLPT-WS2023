# Get the abstract but limited to first 1000 of them

# import subprocess
# import os
# from datetime import datetime

# # Set the path to the edirect folder
# edirect_path = os.path.expanduser("~/edirect")

# # Update the PATH environment variable
# os.environ["PATH"] = f"{edirect_path}:{os.environ['PATH']}"

# # Set the NCBI API key
# os.environ["NCBI_API_KEY"] = "99ceeba4500a64c4c5bfa5fea552ca41d309"

# # Define the search parameters
# search_query = '"intelligence[Title/Abstract] AND 2013/01/01:2023/12/31[Date - Publication]"'

# # Create a timestamp for the output file
# timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
# output_file = f"abstracts_{timestamp}.txt"

# # Construct the command to fetch abstracts
# command = f'esearch -db pubmed -query {search_query} | efetch -format abstract'

# # Run the command and capture the output
# try:
#     result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
#     abstracts = result.stdout
# except subprocess.CalledProcessError as e:
#     print(f"Error: {e}")
#     abstracts = ""

# # Save the abstracts to a text file
# with open(output_file, "w", encoding="utf-8") as file:
#     file.write(abstracts)

# print(f"Abstracts have been saved to {output_file}")


# # Get XML file of abstracts and references
# import requests

# # Specify the database and query parameters
# db = 'pubmed'
# query = 'intelligence[Title/Abstract] AND 2013/01/01:2023/12/31[Date - Publication]'

# # Assemble the ESearch URL
# base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
# esearch_url = f"{base}esearch.fcgi?db={db}&term={query}&usehistory=y"

# # Post the ESearch URL
# esearch_output = requests.get(esearch_url).text

# # Parse WebEnv and QueryKey from the ESearch output
# web = esearch_output.split('<WebEnv>')[1].split('</WebEnv>')[0]
# key = esearch_output.split('<QueryKey>')[1].split('</QueryKey>')[0]

# # EFetch Section
# # Assemble the EFetch URL to fetch abstracts and their references in XML format
# efetch_url = f"{base}efetch.fcgi?db={db}&query_key={key}&WebEnv={web}"
# efetch_url += "&rettype=abstract&retmode=xml&retmax=1000"  # Adjust retmax as needed

# # Post the EFetch URL
# data = requests.get(efetch_url).text

# # Save the abstracts and references to a text file
# output_file = "abstracts_and_references.xml"
# with open(output_file, "w", encoding="utf-8") as file:
#     file.write(data)

# print(f"Abstracts and references have been saved to {output_file}")



import subprocess
import os
from datetime import datetime

# Set the path to the edirect folder
edirect_path = os.path.expanduser("~/edirect")

# Update the PATH environment variable
os.environ["PATH"] = f"{edirect_path}:{os.environ['PATH']}"

# Set the NCBI API key
os.environ["NCBI_API_KEY"] = "99ceeba4500a64c4c5bfa5fea552ca41d309"

# Define the search parameters
search_query = '"intelligence[Title/Abstract] AND 2013/01/01:2023/12/31[Date - Publication]"'

# Create a timestamp for the output file
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

# Construct the command to fetch abstracts and their IDs
esearch_command = f'esearch -db pubmed -query {search_query} -usehistory -retmax 0'

try:
    esearch_result = subprocess.run(esearch_command, shell=True, capture_output=True, text=True, check=True)
    esearch_output = esearch_result.stdout
except subprocess.CalledProcessError as e:
    print(f"Error executing esearch command: {e}")
    print(f"Output: {e.stdout}")
    print(f"Error Output: {e.stderr}")  # Print the error output
    exit(1)

# Extract WebEnv and QueryKey from the esearch output
webenv = esearch_output.split("<WebEnv>")[1].split("</WebEnv>")[0]
querykey = esearch_output.split("<QueryKey>")[1].split("</QueryKey>")[0]

# Set the maximum number of IDs to fetch in each batch
batch_size = 1000

# Fetch abstracts in batches
for start in range(0, int(querykey), batch_size):
    # Construct the command to fetch abstracts for the current batch
    efetch_command = f'esearch -db pubmed -query {search_query} -WebEnv {webenv} -QueryKey {querykey} -retstart {start} -retmax {batch_size} | efetch -format abstract'
    
    try:
        result = subprocess.run(efetch_command, shell=True, capture_output=True, text=True, check=True)
        abstracts = result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing efetch command: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error Output: {e.stderr}")  # Print the error output
        exit(1)

    # Save the abstracts to a text file
    output_file = f"abstracts_{timestamp}_batch_{start // batch_size}.txt"
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(abstracts)

    print(f"Batch {start // batch_size}: Abstracts have been saved to {output_file}")
