import pandas as pd
import glob

files = glob.glob("Articles_*.csv")

dataframes = []

for file in files:
    data = pd.read_csv(file)
    dataframes.append(data)

combined_data = pd.concat(dataframes, ignore_index=True)

combined_data.to_csv("All_articles.csv", index=False)
