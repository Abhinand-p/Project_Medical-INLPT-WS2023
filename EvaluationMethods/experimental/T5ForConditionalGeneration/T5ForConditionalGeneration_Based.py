import pandas as pd
from transformers import T5ForConditionalGeneration, T5Tokenizer
import re

def remove_special_characters(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

data = pd.read_csv('../First_10_Rows.csv')

# Load T5 model and tokenizer
model_name = "t5-base"
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)

# Create a list to hold dictionaries for each row
result_rows = []

# Iterate through the abstracts
for index, row in data.iterrows():
    abstract = row['AB']
    abstract_cleaned = remove_special_characters(abstract)

    # Tokenize and generate a question using T5
    inputs = tokenizer(f"generate a question: {abstract_cleaned}", return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(**inputs, max_length=100, num_beams=4, length_penalty=2.0, early_stopping=True)

    generated_question = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    result_rows.append({
        'PMID': row['PMID'],
        'generated_question': generated_question,
        'AB': abstract
    })

# Create the final DataFrame
result_df_qa = pd.concat([pd.DataFrame([row]) for row in result_rows], ignore_index=True)

# Save the DataFrame to a CSV file
result_df_qa.to_csv('T5ForConditionalGeneration_Based_QA.csv', index=False)
