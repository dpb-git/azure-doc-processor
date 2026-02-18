# Azure Document Processor Function
import azure.functions as func
import logging
import os
from azure.cosmos import CosmosClient
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from datetime import datetime

app = func.FunctionApp()

# Initialize Cosmos client
cosmos_client = CosmosClient.from_connection_string(os.environ["COSMOS_CONNECTION"])
database = cosmos_client.get_database_client("documentdb")
container = database.get_container_client("documents")

# Initialize Document Intelligence client
doc_intelligence_client = DocumentAnalysisClient(
    endpoint=os.environ["DOCUMENT_INTELLIGENCE_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["DOCUMENT_INTELLIGENCE_KEY"])
)

@app.blob_trigger(
    arg_name="myblob",
    path="uploads/{name}",
    connection="STORAGE_CONNECTION"
)
def ProcessDocument(myblob: func.InputStream):
    logging.info(f"Processing file: {myblob.name}")
    
    # Read the file content
    file_bytes = myblob.read()
    
    # Analyze document with AI
    poller = doc_intelligence_client.begin_analyze_document(
        "prebuilt-read", file_bytes
    )
    result = poller.result()
    
    # Extract all text
    extracted_text = ""
    for page in result.pages:
        for line in page.lines:
            extracted_text += line.content + "\n"
    
    # Create document to store in Cosmos
    document = {
        "id": myblob.name.replace("uploads/", ""),
        "filename": myblob.name.replace("uploads/", ""),
        "size": myblob.length,
        "processed_at": datetime.utcnow().isoformat(),
        "status": "processed",
        "extracted_text": extracted_text.strip(),
        "page_count": len(result.pages)
    }
    
    # Save to Cosmos DB
    container.upsert_item(document)
    logging.info(f"Saved to Cosmos DB: {document['filename']} ({document['page_count']} pages)")
