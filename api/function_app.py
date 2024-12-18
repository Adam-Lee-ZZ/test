import azure.functions as func
import logging
from getlist import get_list
from azure.storage.blob import BlobServiceClient
import os

def upload_to_blob_storage(file_path: str, blob_name: str):
    """Uploads a file to Azure Blob Storage."""
    connection_string = "your_connection_string"  # Replace with your Azure Blob Storage connection string
    container_name = "your_container_name"  # Replace with your container name

    # Initialize BlobServiceClient using connection string
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    
    # Get the container client
    container_client = blob_service_client.get_container_client(container_name)
    
    # Upload the file to the specified container in Blob Storage
    with open(file_path, "rb") as data:
        container_client.upload_blob(blob_name, data, overwrite=True)  # `overwrite=True` allows overwriting existing files

def main(req: func.HttpRequest) -> func.HttpResponse:
        # Parse the JSON request data
        data = req.get_json()

        # Extract user input from the request data
        user_input = data['inputData']

        # Get the playlist data
        ll = get_list(user_input)

        # Initialize an empty string to build the HTML response
        body = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PlaylistMotion</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style_sub.css') }}">
</head>
<body>
    <div class="header"><h1>PlaylistMotion</h1></div>
    <div class="pale"></div><div class="pale"></div>
    <div><p class="description"><strong>## Please select the proper playlist. ##</strong></p></div>
    <div class="pale"></div><div class="pale"></div>'''

        # Iterate over the rows to add them to the HTML
        for index, line in ll.iterrows():
            if line[0] != '':
                body += f'''
        <div class="playlist-card">
            <img src="{line[2]}" alt="Playlist Image">
            <h3>{line[3]}</h3>
            <p>Creator: {line[4]}</p>
            <p><h2>{line[1]}</h2></p>
            <div class="pale"></div>
            <button class="selectbutton" onclick="selectData(event)">Select</button>
        </div>
        <div class="pale"></div>'''

        body += '''
</body>
</html>'''

        # Define the path to save the HTML file in the /tmp directory (which is writable in Azure Functions)
        html_file_path = '/tmp/playlist.html'  # Path for temporary file storage in Azure Functions

        # Write the HTML body to a file
        with open(html_file_path, 'w') as f:
            f.writ
