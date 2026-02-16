import azure.functions as func
import logging

app = func.FunctionApp()

@app.blob_trigger(
    arg_name="myblob",
    path="uploads/{name}",
    connection="STORAGE_CONNECTION"
)
def ProcessDocument(myblob: func.InputStream):
    logging.info(f"Processing file: {myblob.name}")
    logging.info(f"File size: {myblob.length} bytes")