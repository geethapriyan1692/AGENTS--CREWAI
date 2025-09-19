import json
import requests

def Address_Agent_Process(agentOutput, payload):
    payload = json.dumps(payload)
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post('https://dev-mlaa-g7-product.excelacom.in/centuryServiceAPI/v1/validateAddress', data=payload, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        if hasattr(e, 'request'):
            return f"Error: {e.request}"
        else:
            return f"Error: {e}"
import json
import requests

def Address_Serviceability_Agent(agentOutput, payload):
    try:
        json_payload = json.dumps(payload)
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.post('https://devqa1-g7-product.excelacom.in/centuryServiceAPI/v1/launchProcessPlan', headers=headers, data=json_payload)
        return response.text
    except requests.exceptions.RequestException as e:
        if hasattr(e, 'request'):
            return f"Error: {e.request}"
        else:
            return f"Error: {e}"
import json
import requests

def Service_Availability_Agent(agentOutput, payload):
    url = "https://dev-mlaa-g7-product.excelacom.in/centuryServiceAPI/v1/checkAvailability"
    headers = {
        'Content-Type': 'application/json',
    }
    data = json.dumps(payload)
    try:
        response = requests.post(url, headers=headers, data=data)
        return response.text
    except requests.exceptions.RequestException as e:
        if hasattr(e, 'request'):
            return f"Error: {e}"
        else:
            return f"Error: {e}"
import json
import requests

def Serviceability_Agent(agentOutput, payload):
    url = "https://devqa1-g7-product.excelacom.in/centuryServiceAPI/v1/checkAvailability"
    headers = {
        'Content-Type': 'application/json',
    }
    data = json.dumps(payload)
    try:
        response = requests.post(url, headers=headers, data=data)
        return response.text
    except requests.exceptions.RequestException as e:
        if hasattr(e, 'request'):
            return f"Error: {e}"
        else:
            return f"Error: {e}"
import json
import requests

def Testing_Agent(agentOutput, payload):
    headers = {'Content-type': 'application/json'}
    data = json.dumps(payload)
    try:
        response = requests.post('https://dummyjson.com/products/add', headers=headers, data=data)
        return response.text
    except requests.exceptions.RequestException as e:
        if hasattr(e, 'request'):
            return f"An error occurred: {e}"
        else:
            return f"An error occurred: {e}"




import json
import requests

def Address_Validation_Agent(agentOutput, payload):
    url = "https://devqa1-g7-product.excelacom.in/centuryServiceAPI/v1/checkAvailability"
    headers = {
        'Content-Type': 'application/json',
    }
    data = json.dumps(payload)
    try:
        response = requests.post(url, headers=headers, data=data)
        return response.text
    except requests.exceptions.RequestException as e:
        if hasattr(e, 'request'):
            return f"Error: {e}"
        else:
            return f"Error: {e}"
import json
import requests

def Seviceability_validation(agentOutput, payload):
    headers = {'Content-type': 'application/json'}
    data = json.dumps(payload)
    try:
        response = requests.post('https://dummyjson.com/products/add', headers=headers, data=data)
        return response.text
    except requests.exceptions.RequestException as e:
        if hasattr(e, 'request'):
            return f"An error occurred: {e}"
        else:
            return f"An error occurred: {e}"

