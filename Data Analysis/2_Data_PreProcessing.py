import re
import pandas as pd


def read_input_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        input_text = f.read()
    return input_text


def split_articles(input_text):
    articles = re.split(r'\n"\n', input_text.strip())
    return articles


def extract_data(article):
    data = {}
    current_key = None
    current_value = ''

    for line in article.split('\n'):
        match = re.match(r'^([A-Z]{2,4})\s*- (.+)$', line)
        if match:
            key, value = match.groups()
            if current_key:
                data[current_key] = data.get(current_key, '') + '|' + current_value.strip()
                current_value = ''

            current_key, current_value = key, value
        else:
            current_value += ' ' + line.strip()

    if current_key:
        data[current_key] = current_value.strip()

    return data


def process_articles(articles):
    article_data_list = [extract_data(article) for article in articles]
    total_articles_before = len(article_data_list)

    filtered_data_list = [data for data in article_data_list if 'AB' in data]
    total_articles_after = len(filtered_data_list)

    columns_to_keep = ['PMID', 'TI', 'AB', 'PB', 'FAU', 'FED', 'DP', 'OTO', 'OT', 'OWN', 'DCOM', 'LR', 'JT', 'MH',
                       'ISBN']
    df = pd.DataFrame(filtered_data_list)[columns_to_keep]

    # To drop duplicates
    df = df.drop_duplicates(subset='PMID', keep='first')

    return total_articles_before, total_articles_after, df


def save_to_csv(data_frame, file_path):
    data_frame.to_csv(file_path, index=False)


def main():
    input_file = 'All_articles.csv'
    output_file = 'All_Articles_PreProcessed.csv'

    input_text = read_input_file(input_file)
    articles = split_articles(input_text)
    total_before, total_after, processed_df = process_articles(articles)
    save_to_csv(processed_df, output_file)

    print(f"Number of articles before cleaning: {total_before}")
    print(f"Number of articles after cleaning: {total_after}")

    # Random Row
    if not processed_df.empty:
        print("\nRandom Row:")
        random_row = processed_df.sample()
        print(random_row)


if __name__ == "__main__":
    main()
