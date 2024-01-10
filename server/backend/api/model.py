import json
import pandas as pd
from fastapi import Header, APIRouter
from azure.ai.ml import MLClient
from azure.identity import (
    DefaultAzureCredential,
    InteractiveBrowserCredential,
)

def get_data(question, context):
    print(type(question),type(context))
    try:
        credential = DefaultAzureCredential()
        credential.get_token("https://management.azure.com/.default")
    except Exception as ex:
        credential = InteractiveBrowserCredential()

    workspace_ml_client = MLClient(
        credential,
        subscription_id="5eec2903-9705-470a-835a-0221fbc8d93d",
        resource_group_name="inlpt",
        workspace_name="MLINLPT",
    )
    online_endpoint_name = "biobert-pubmed-qa"
    deployment_name = "nlpt-biobert"


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

    response = workspace_ml_client.online_endpoints.invoke(
        endpoint_name=online_endpoint_name,
        deployment_name=deployment_name,
        request_file="./query.json",
    )
    print("raw response: \n", response, "\n")
    # convert the json response to a pandas dataframe
    response_df = pd.read_json(response)

    return response_df[0][0]