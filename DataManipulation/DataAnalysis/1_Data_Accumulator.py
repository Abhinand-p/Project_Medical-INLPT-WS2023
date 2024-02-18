import pandas as pd
import glob

# Change the path accordingly
files = glob.glob("/Users/abhinandp/PycharmProjects/project-INLPT-WS2023/Data Pool/Data/Articles_*.csv")

dataframes = []

for file in files:
    data = pd.read_csv(file)
    dataframes.append(data)

combined_data = pd.concat(dataframes, ignore_index=True)

combined_data.to_csv("All_articles.csv", index=False)
