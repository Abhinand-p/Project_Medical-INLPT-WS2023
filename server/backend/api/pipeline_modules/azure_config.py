import json
import time
import pandas as pd
from fastapi import Header, APIRouter
import os
from dotenv import load_dotenv
from azure.ai.ml import MLClient
from azure.ai.ml.entities import ManagedOnlineEndpoint, ManagedOnlineDeployment
from azure.identity import InteractiveBrowserCredential, ClientSecretCredential, DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

class AzureManager:
    def __init__(self):
        load_dotenv()
        try:
            credential = DefaultAzureCredential()
            credential.get_token("https://management.azure.com/.default")
        except Exception as ex:
            credential = InteractiveBrowserCredential()

        try:
            self.workspace_ml_client = MLClient(
                credential,
                subscription_id= os.getenv("AZURE_SUBSCRIPTION_KEY"),
                resource_group_name=os.getenv("RESOURCE_GROUP_NAME"),
                workspace_name=os.getenv("WORKSPACE_NAME"))

            self.deployment_name = os.getenv("DEPLOYMENT_NAME")

            registry_name = "HuggingFace"
            model_name = "biobert-pubmed-qa"
            model_id = f"azureml://registries/{registry_name}/models/{model_name}/labels/latest"

            self.online_endpoint_name=os.getenv("ONLINE_ENDPOINT_NAME") + "-" + str(int(time.time())) # endpoint name must be unique per Azure region, hence appending timestamp
            endpoint = self.workspace_ml_client.begin_create_or_update(ManagedOnlineEndpoint(name=self.online_endpoint_name) ).wait()
            self.workspace_ml_client.online_deployments.begin_create_or_update(ManagedOnlineDeployment(
                name=self.deployment_name,
                endpoint_name=self.online_endpoint_name,
                model=model_id,
                instance_type="Standard_DS2_v2",
                instance_count=1,
            )).wait()
            endpoint.traffic = {self.deployment_name: 100}
            self.workspace_ml_client.begin_create_or_update(self.online_endpoint_name).result()
        except Exception as ex:
            print(ex)

    def query(self, question, context):
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
            request_file="./query.json")
        # print("raw response: \n", response, "\n")

        with open("response.json", "w") as f:
            json.dump(response, f)

        data = ''
        with open('./response.json', 'r') as f:
            data = json.load(f)

        response_df = pd.read_json(data, lines=True)

        # return the answer with the highest score
        return response_df.loc[response_df['score'].idxmax()]['answer']