## Live Demo

Upload a PDF at https://polite-flower-01b23d00f.2.azurestaticapps.net stored in Cosmos DB with extracted text.

# Azure Document Processor

A cloud-based document processing pipeline built on Microsoft Azure. Users upload a PDF through a web interface and the system automatically extracts all text using AI, then stores it in a database for querying.

## What it does

Upload a PDF and within seconds the system has read it, extracted every word, and stored the results in a searchable database. No manual steps needed.

## Architecture

1) User uploads a PDF
2) Azure Blob Storage (the filing cabinet where uploaded files live)
3) Azure Functions (the automatic worker that detecs new files and triggers the pipleine)
4) Azure AI Document Intelligence (reads the document and extracts all text)
5) Cosmos DB (the organized filing system where extracted text is stored allowing for queries)

## Azure Services used

Azure Blob Storage - When someone uploads a PDF, it lands here first. Every file is stored safely in the cloud regardless of how many users are uploading at the same time.

Azure Functions - When a file arrives in Blob, Functions detects it instantly and triggers the processing pipeline without anyone pressing a button. This is serverless. Only runs when a file arrives.

Azure AI Document Intelligence - Opens the uploaded PDF and extracts every word from every page, turning an unreadable blob of bytes in usable text.

Cosmos DB - Once text is extracted it gets stored here as a JSON document alongside metadata like filename, page count, file size, and timestamp. You can query it, search it, and build on top of it.

## How to run locally

### Prereqs

- Azure account
- Python 3.11+
- Azure Functions Core Tools v4
- Azure CLI

### Setup 

1. Clone the repository
   git clone https://github.com/dpb-git/azure-doc-processor.git
   cd azure-doc-processor

2. Install dependencies
   pip install -r requirements.txt

3. Configure local settings
   Add your connection strings to local.settings.json:
   - AzureWebJobsStorage
   - STORAGE_CONNECTION
   - COSMOS_CONNECTION
   - DOCUMENT_INTELLIGENCE_ENDPOINT
   - DOCUMENT_INTELLIGENCE_KEY

4. Start the function
   func start

5. Open the frontend
   cd frontend
   python -m http.server 8000
   Navigate to http://localhost:8000

## What I learned

- How to build an event-driven architecture on Azure
- How serverless functions react to cloud events automatically
- How to integrate Azure AI services into a real pipeline
- How to store and structure data in Cosmos DB
- How to connect a web frontend directly to Azure Blob Storage