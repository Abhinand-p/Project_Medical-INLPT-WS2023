# "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"

import os
from openai import OpenAI, OpenAIError
import pandas as pd
import re

# Set your OpenAI API key
api_key = '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'

# Check if the API key is provided
if not api_key:
    raise OpenAIError("The API key must be set. Please provide your OpenAI API key.")

client = OpenAI(api_key=api_key)

# Load the PubMed CSV file
data = pd.read_csv('../First_10_Rows.csv')

# Function to remove special characters
def remove_special_characters(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

# Prepare messages for GPT-3
messages = [{"role": "user", "content": ""}]  # Initial empty message

# Iterate through the abstracts
for abstract in data['AB']:
    # Remove special characters from the abstract
    abstract = remove_special_characters(abstract)

    # Add user message to prompt GPT-3 for question generation
    messages[-1]["content"] = f"Generate a question based on the following text: {abstract}"

    # Generate a question using GPT-3.5 Turbo
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    # Extract the generated question from the GPT-3 response using the get method
    question = chat_completion.get('choices', [{}])[0].get('message', {}).get('content', '').strip()

    print(f'Question: {question}')
    print()

