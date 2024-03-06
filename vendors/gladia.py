import requests
import os
import time

from dotenv import load_dotenv

load_dotenv()

log = False

def translate(file_path, language='en', target_lang='es', model='enhanced'):

    def make_request(url, headers, method="GET", data=None, files=None):
        if method == "POST":
            response = requests.post(url, headers=headers, json=data, files=files)
        else:
            response = requests.get(url, headers=headers)
        return response.json()

    if os.path.exists(file_path):  # This is here to check if the file exists
        if log:
            print("- File exists")
    else:
        if log:
            print("- File does not exist")
        return None, None

    file_name, file_extension = os.path.splitext(
        file_path
    )  # Get your audio file name + extension

    with open(file_path, "rb") as f:  # Open the file
        file_content = f.read()  # Read the content of the file

    headers = {
        "x-gladia-key": os.getenv("GLADIA", ""),  # Replace with your Gladia Token
        "accept": "application/json",
    }

    files = [("audio", (file_path, file_content, "audio/" + file_extension[1:]))]
    
    if log:
        print("- Uploading file to Gladia...")
    upload_response = make_request(
        "https://api.gladia.io/v2/upload/", headers, "POST", files=files
    )

    if log:
        print("Upload response with File ID:", upload_response)
    audio_url = upload_response.get("audio_url")

    data = {
        "audio_url": audio_url,
        "translation": True,
        "translation_config": {
            "target_languages": [target_lang],
            "model": "enhanced",
        },
        "language": language,
    }
    # You can also send an URL directly without uploading it. Make sure it's the direct link and publicly accessible.
    # For any parameters, please see: https://docs.gladia.io/reference/pre-recorded

    headers["Content-Type"] = "application/json"
    
    if log:
        print("- Sending request to Gladia API...")
    post_response = make_request(
        "https://api.gladia.io/v2/transcription/", headers, "POST", data=data
    )

    if log:
        print("Post response with Transcription ID:", post_response)
    result_url = post_response.get("result_url")

    if result_url:
        start = time.time()
        while True:
            if log:
                print("Polling for results...")
            poll_response = make_request(result_url, headers)

            if poll_response.get("status") == "done":
                if log:
                    print("- Transcription done: \n")
                    # print(poll_response.get("result"))
                    print(poll_response.get("result").get("translation"))
                end = time.time()
                try:
                    result = poll_response["result"]["translation"]["results"][0]["full_transcript"]
                    time_taken = end - start
                except KeyError:
                    result = None
                    time_taken = None
                return result, time_taken
            
            elif poll_response.get("status") == "error":
                if log:
                    print("- Transcription failed")
                    print(poll_response)
            else:
                if log:
                    print("Transcription status:", poll_response.get("status"))
            time.sleep(1)

    if log:
        print("- End of work")