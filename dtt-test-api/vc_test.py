import os
import json
import requests



def send_api_request(payload):
    """Send an API request with the given payload."""
    url = "http://localhost:8000/api/v1/test-suites/credentials/w3c"
    headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRfaWQiOiIzZGZlZjgxMi0wYzFlLTVkMzctOTI3MS01OTAyMThmNGY1NTYiLCJleHBpcmVzIjoxNzE2NDE1NTUxfQ.J6nvrhHxO-4Kw-phbYT2O4tdwKDwRNDKgOP7ot8W7VU'
            }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.status_code, response.text

def read_payloads_from_folder(folder_path):
    """Read JSON payloads from each file in the specified folder."""
    folder_path = 'tests_scripts/input'
    payloads = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".jsonld"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                payload = {"verifiableCredential":json.load(file)}
                payloads.append(payload)
    return payloads

def main():
    folder_path = './test_script/input'
    payloads = read_payloads_from_folder(folder_path)
    
    for payload in payloads:
        status_code, response_text = send_api_request(payload)
        if(status_code == 200):
            print(f"test passed")
        else:
            print(f"Response from API: Status {status_code} failed file {payload}" )
            print(f"Failed file  :  {payload} \n\r" )

if __name__ == "__main__":
    main()
