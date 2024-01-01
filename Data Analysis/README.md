# Data Analysis
This repository contains codes used to perform data-analysis of the extracted dataset from PubMed.

## 1. Data Accumulation
### Step 1: Execute Data_Accumulator.py
1. This accumulates all the yearly extracted data to a single file: All_articles.csv
2. This is perfomed in order to avoid pushing large files to github. 

## 2. Data Pre-Processing
### Step 1: Execute Data_PreProcessing.py
1. This step is performed to gather required data filed.     
2. It stores the columns of ['PMID', 'TI', 'AB', 'PB', 'FAU', 'FED', 'DP', 'OTO', 'OT', 'OWN', 'DCOM', 'LR', 'JT', 'MH','ISBN']
3. This code also removes duplicates based on PMID
4. Output:
   <code> Number of articles before cleaning: 79640</code>
   <code>Number of articles after cleaning: 74243 </code>

## 3. Data Analysis 
### Refer the Data_Analysis.ipynb jupyter notebook 
|                   |                           Title Analysis                           |                            Abstract Analysis                             |
|-------------------|:------------------------------------------------------------------:|:------------------------------------------------------------------------:|
| Distribution Plot | ![TitlesDistributionPlot.png](Images%2FTitlesDistributionPlot.png) | ![AbstractsDistributionPlot.png](Images%2FAbstractsDistributionPlot.png) |
| Word Cloud        |        ![TitlesWordCloud.png](Images%2FTitlesWordCloud.png)        |        ![AbstractsWordCloud.png](Images%2FAbstractsWordCloud.png)        |