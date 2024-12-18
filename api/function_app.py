import azure.functions as func
import logging
import os
import base64
import requests
from getlist import get_list

GITHUB_API_URL = "https://api.github.com"
REPO_OWNER = "Adam-Lee-ZZ"
REPO_NAME = "test1"
FILE_PATH = "/tmp/playlist.html"
BRANCH = "main"  # Or the branch where you want to upload the file
GITHUB_TOKEN = "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en"  # Replace with your GitHub Personal Access Token

def upload_to_github(file_path: str, file_name: str):
    """Upload a file to GitHub using the GitHub API."""
    
    # Read the file content and encode it in base64
    with open(file_path, "rb") as file:
        file_content = base64.b64encode(file.read()).decode('utf-8')

    # Get the file's current state on GitHub (check if it exists, to determine whether to create or update)
    url = f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_name}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Fetch the file's current info to get the SHA for update
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        # If file exists, we need the SHA to update it
        file_info = response.json()
        sha = file_info['sha']
        commit_message = "Updating playlist.html"
    else:
        # If file doesn't exist, we don't need SHA
        sha = None
        commit_message = "Creating playlist.html"

    # Prepare the data for the API request
    data = {
        "message": commit_message,
        "content": file_content,
        "branch": BRANCH,
    }
    if sha:
        data["sha"] = sha
    
    # Upload or update the file via the API
    response = requests.put(url, json=data, headers=headers)

    if response.status_code == 201 or response.status_code == 200:
        logging.info("File uploaded successfully!")
    else:
        logging.error(f"Error uploading file to GitHub: {response.status_code} - {response.text}")

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
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
            f.write(body)

        # Upload the HTML file to GitHub
        upload_to_github(html_file_path, "playlist.html")

        # Optionally, export the body if needed (depending on the external getlist.export function)
        get_list.export(body)

        # Return a response indicating success
        return func.HttpResponse(f"HTML file saved and uploaded to GitHub as 'playlist.html'", status_code=200)

    except Exception as e:
        # Log any error that occurs
        logging.error(f"Error processing the request: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)
