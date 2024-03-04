# Getting Started Docker

This project was bootstrapped with [docker](https://www.docker.com/).

## Available Scripts

In the project directory, you can run:

### `docker compose -f .\docker-compose.yml up` [Get started with docker compose](https://docker-docs.uclv.cu/compose/gettingstarted/)

Docker Compose is a tool that was developed to help define and share multi-container applications. With Compose, we can create a YAML file to define the services and with a single command, can spin everything up or tear it all down.

### Check the YAML file here [docker-compose.yml](./docker-compose.yml)

1. You can find under the yaml file by the light backend server under the enviroment field variables are needed to boot up the system properly

    - **OPENAI_API_KEY**=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
    - **HF_AUTH**=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
    - **VOYAGE_API_KEY**=pa-pBWwn664zrcc-80y0pFExXwjRuCKQhygngCFq7DT4d
    - **AZURE_SUBSCRIPTION_KEY**=5eec2903-9705-470a-835a-0221fbc8d93d
    - **RESOURCE_GROUP_NAME**=inlpt-azure-ml
    - **WORKSPACE_NAME**=MLINLPT-Azure-ml
    - **ONLINE_ENDPOINT_NAME**=biobert-pubmed-ml
    - **DEPLOYMENT_NAME**=nlpt-biobert-ml

2. It is really **important** to run this **command** `sudo sysctl -w vm.max_map_count=262144` on wsl before running the opensearch sever up so the server can run up properly

3. Azure pipeline requires some variable input that can be changed according to your will of deployment as the pipeline does create the whole process on initialization and make it ready for you to use. Till now we did a default endpoint using `ktrapeznikov-biobert-v1.1-pubmed-squad-v2` with small compute resources. The variables are self explainatory if you follow with these two Microsoft blogs under Learn platform [Machine Learning workspaces](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-manage-workspace?view=azureml-api-2&tabs=python) / [Machine Learning online endpoint](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-deploy-models-from-huggingface?view=azureml-api-2)

## Learn More

You can learn more in the [Docker Docs](https://docs.docker.com/)
