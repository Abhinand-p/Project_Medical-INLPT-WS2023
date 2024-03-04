# Getting Started with FastAPI and Uvicorn (no docker)

This project was done with [FastApi](https://fastapi.tiangolo.com/tutorial/) and [Uvicorn](https://www.uvicorn.org/).

## Step 1: Installation

In the project directory, you can run:

1. `pip install fastapi`
2. `pip install uvicorn`

## Step 2: Deployment

To run the backend server we need to use Uvicorn for that to instantiate the required REST API.

`uvicorn main:app` which will select a random port on bootup

for specific port you can do the following:

`uvicorn main:app --reload --port:8000` Note: The server will reload if you make edits on the code due to `--reload` flag.

## Learn More

You can learn more please refer to [FastAPI](https://fastapi.tiangolo.com/reference/) & [Uvicorn](https://www.uvicorn.org/deployment/).
