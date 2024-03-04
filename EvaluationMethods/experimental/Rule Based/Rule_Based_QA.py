import pandas as pd
import re

data = pd.read_csv('../First_10_Rows.csv')

def remove_special_characters(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

def generate_rule_based_question(abstract):

    # Questions for different patterns
    found_words_investigate = []
    question_investigate = "Did the study specifically aim to investigate?"

    found_words_method = []
    question_method = "Did the study specifically use a method or approach?"

    found_words_result = []
    question_result = "Did the study specifically report results or findings?"

    # Regular expressions and matching
    if match := re.search(r'\b(?:investigate)\b', abstract, re.IGNORECASE):
        found_words_investigate.append(match.group(0))

    if match := re.search(r'\b(?:method|procedure|approach)\b', abstract, re.IGNORECASE):
        found_words_method.append(match.group(0))

    if match := re.search(r'\b(?:result|finding|outcome)\b', abstract, re.IGNORECASE):
        found_words_result.append(match.group(0))

    # Confirmation questions and answers
    answer_investigate = 'Yes' if found_words_investigate else 'No'
    answer_method = 'Yes' if found_words_method else 'No'
    answer_result = 'Yes' if found_words_result else 'No'

    return answer_investigate, answer_method, answer_result

result_rows = []

for index, row in data.iterrows():
    abstract = remove_special_characters(row['AB'])

    answer_investigate, answer_method, answer_result = generate_rule_based_question(abstract)

    result_rows.append({
        'PMID': row['PMID'],
        'question_investigate': answer_investigate,
        'question_method': answer_method,
        'question_result': answer_result,
        'AB': row['AB']
    })

result_df_qa = pd.concat([pd.DataFrame([row]) for row in result_rows], ignore_index=True)

result_df_qa.to_csv('Rule_Based_QA.csv', index=False)
