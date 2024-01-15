# Evaluation Methods for benchmark dataset based on generating questions 
This repository contains codes used to perform question generation that can be used as a metric.

## 1. Rule Based
### Notes
1. This method can be used to generate Confirmation Questions based on the set regular expression.
2. The method is easy to implement and scale based on the selected words.

## 2. BioBERT Based
### Notes
1. This method uses the pretrained BioBERT model to generate the questions.
2. Pre-training would be required to obtain an optimal question generation.
3. Further checking is required to improve the quality of questions generated here.

## 3. T5ForConditionalGeneration Based
### Notes
1. This method uses the T5ForConditionalGeneration model to generate the questions.
2. Similar to BioBART based this would also require pre-training.

## 4. ChatGPT API Based
### Notes
1. With the new rules of free tier, it shows "You exceeded your current quota, please check your plan and billing details"
2. This method would be optimal to generate the questions in detail.
3. This method would also be the easiest when prompt engineering is done.
