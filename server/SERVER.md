# Documentation

This end-to-end chatbot application is realized by a locally hosted website through which the user can chat to the model

## Frontend

- Built with NodeJS, TypeScript, React and NextJS
- Features: Access model over a chat component
- Addtional pages f.e. About, Settings, Contact pages

## Backend

- Built with FastAPI and UVICORN
- Access point for frontend to our pipeline

## Pipeline

- Embedding models (voyage-2-large, text-embedding-3-large, distilroberta, e5-base-v2)
- Vector Store (Opensearch)
- Models ("GPT 3.5 Turbo 0125", "GPT 3.5 Turbo 0125 (Langchain)", "LLAMA-2-7b-chat-hf", "Azure-Biobert-Pubmed-QA")

## Step by step

- Once pulled navigate to .../server/frontend and type in: "npm install" this will install all necessary frontend libraries
- In the same directory open a terminal and type in: "npm run dev" to run the frontend server
- navigate to .../server/backend and install uvicorn and fastapi
- In the same directory open a terminal and type in: "uvicorn main:app --reload"
- now go to your browser and open: "localhost:3000"
