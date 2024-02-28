import json
import pandas as pd
from fastapi import Header, APIRouter
from dotenv import load_dotenv
from azure.ai.ml import MLClient
from azure.identity import (
    DefaultAzureCredential,
    InteractiveBrowserCredential,
)

class AzureManager:
    def __init__(self):
        load_dotenv()
        try:
            credential = DefaultAzureCredential()
            credential.get_token("https://management.azure.com/.default")
        except Exception as ex:
            credential = InteractiveBrowserCredential()

        self.workspace_ml_client = MLClient(
            credential,
            subscription_id="5eec2903-9705-470a-835a-0221fbc8d93d",
            resource_group_name="inlpt",
            workspace_name="MLINLPT",
        )
        self.online_endpoint_name = "biobert-pubmed-qa"
        self.deployment_name = "nlpt-biobert"

    def query(self, question, context):
        # print(type(question),type(context))

        question = question.replace("'", "\\'").replace('"', '\\"')
        context = context.replace("'", "\\'").replace('"', '\\"')

        # create a json object with the key as "inputs" and value as a list of question-context pairs
        query_json = {
            "inputs": {
                "question": question,
                "context": context,
            }
        }
        # save the json object to a file named sample_score.json in the ./squad-dataset folder
        with open("query.json", "w") as f:
            json.dump(query_json, f)

        response = self.workspace_ml_client.online_endpoints.invoke(
            endpoint_name=self.online_endpoint_name,
            deployment_name=self.deployment_name,
            request_file="./query.json",
        )
        # print("raw response: \n", response, "\n")

        with open("response.json", "w") as f:
            json.dump(response, f)

        data = ''
        with open('./response.json', 'r') as f:
            data = json.load(f)

        response_df = pd.read_json(data, lines=True)

        # return the answer with the highest score
        return response_df.loc[response_df['score'].idxmax()]['answer']