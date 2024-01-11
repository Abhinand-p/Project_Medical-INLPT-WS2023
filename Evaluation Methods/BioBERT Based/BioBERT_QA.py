from transformers import BertForQuestionAnswering, BertTokenizer
import pandas as pd
import torch
import re

def remove_special_characters(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

data = pd.read_csv('../First_10_Rows.csv')

# Load BioBERT model and tokenizer
model_name = "dmis-lab/biobert-v1.1"
model = BertForQuestionAnswering.from_pretrained(model_name)
tokenizer = BertTokenizer.from_pretrained(model_name)

result_rows = []

for index, row in data.iterrows():
    abstract = remove_special_characters(row['AB'])

    # Tokenize
    inputs = tokenizer(abstract, return_tensors="pt", max_length=512, truncation=True)
    outputs = model(**inputs)

    start_idx = torch.argmax(outputs.start_logits)
    end_idx = torch.argmax(outputs.end_logits)

    # Generate a question using BioBERT
    generated_question = tokenizer.decode(inputs['input_ids'][0][start_idx:end_idx+1], skip_special_tokens=True).strip()

    result_rows.append({
        'PMID': row['PMID'],
        'generated_question': generated_question,
        'AB': abstract
    })

result_df_qa = pd.concat([pd.DataFrame([row]) for row in result_rows], ignore_index=True)
result_df_qa.to_csv('BioBERT_Based_QA_qa.csv', index=False)
