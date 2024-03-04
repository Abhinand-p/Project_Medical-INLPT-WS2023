import json
import time
import pandas as pd
from fastapi import Header, APIRouter
import os
from azure.mgmt.resource import ResourceManagementClient
from azure.ai.ml import MLClient
from azure.ai.ml.entities import ManagedOnlineEndpoint, ManagedOnlineDeployment, Workspace
from azure.identity import InteractiveBrowserCredential, ClientSecretCredential, DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from dotenv import load_dotenv, find_dotenv

class AzureManager:
    def __init__(self):
        self.msg = ""
        try:
            # Load .env file
            load_dotenv(dotenv_path=find_dotenv())
            print("######### AZURE #############")
            print(os.getenv("HF_AUTH"))
            print(os.getenv("OPENAI_API_KEY"))
            print(os.getenv("VOYAGE_API_KEY"))
            print("#############################")

            # Get Azure credentials
            try:
                credential = DefaultAzureCredential()
                credential.get_token("https://management.azure.com/.default")
            except Exception as ex:
                credential = InteractiveBrowserCredential()

            # Create a resource group
            resource_client = ResourceManagementClient(credential, os.getenv("AZURE_SUBSCRIPTION_KEY"))
            try:
                _ = resource_client.resource_groups.get(os.getenv("RESOURCE_GROUP_NAME"))
            except:
                _ = resource_client.resource_groups.create_or_update(
                    os.getenv("RESOURCE_GROUP_NAME"),
                    {
                        "location": "westeurope"
                    }
                )

            # Create a workspace
            self.workspace_ml_client = MLClient(
                credential,
                subscription_id=os.getenv("AZURE_SUBSCRIPTION_KEY"),
                resource_group_name=os.getenv("RESOURCE_GROUP_NAME"),
                workspace_name=os.getenv("WORKSPACE_NAME"))

            try:
                ws = self.workspace_ml_client.workspaces.get(os.getenv("WORKSPACE_NAME"))
            except:
                ws = Workspace(
                    name=os.getenv("WORKSPACE_NAME"),
                    location="westeurope",
                    display_name="ML Workspace",
                    description="ML Workspace",
                    hbi_workspace=False,
                )

                ws = self.workspace_ml_client.workspaces.begin_create(ws).result()

            # Create deployment
            self.deployment_name = os.getenv("DEPLOYMENT_NAME")

            registry_name = "HuggingFace"
            model_name = "ktrapeznikov/biobert_v1.1_pubmed_squad_v2"
            model_id = f"azureml://registries/{registry_name}/models/{model_name}/labels/latest"

            self.online_endpoint_name=os.getenv("ONLINE_ENDPOINT_NAME")
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
            self.msg = ex

    def query(self, question, context):
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
            endpoint_name="mlinlpt-az-mhimp", # self.online_endpoint_name,
            deployment_name="ktrapeznikov-biobert-v1-1-pub-3", # self.deployment_name,
            request_file="./query.json")
        print("raw response: \n", response, "\n")

        with open("response.json", "w") as f:
            json.dump(response, f)

        data = ''
        with open('./response.json', 'r') as f:
            data = json.load(f)

        response_df = pd.read_json(data, lines=True)

        # return the answer with the highest score
        return response_df.loc[response_df['score'].idxmax()]['answer']

    def azure_info(self):
        return self.workspace_ml_client.info()

    def azure_status(self):
        return "true" if self.msg == "" else "false"