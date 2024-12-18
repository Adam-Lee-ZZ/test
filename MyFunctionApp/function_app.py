import azure.functions as func
import datetime
import json
import logging
from getlist import get_list

app = func.FunctionApp()

# 儲存數據的變量
data = ""

def main(req: func.HttpRequest) -> func.HttpResponse:
    global data

    # 取得用戶的輸入數據
    user_input = req.params.get('inputField')
    
    if not user_input:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            user_input = req_body.get('inputField')

    if user_input:
        # 儲存用戶的輸入
        data = user_input
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

        # Optionally, export the body if needed (depending on the external getlist.export function)
        get_list.export(body)

        # Return a response indicating success
        return func.HttpResponse(f"HTML file saved and uploaded to GitHub as 'playlist.html'", status_code=200)
    else:
        return func.HttpResponse(
             "Please pass an input in the request body",
             status_code=400
        )
    
    
