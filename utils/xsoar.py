import requests
import json

from utils.constants import *

def get_xsoar_incident(sentinel_incident_number: int):
    """ Retrieve the Cortex XSOAR incident with Microsoft Sentinel incident number. """
    incident_uri = f"{XSOAR_URL}/incidents/search"


    incident_search_body = {"userFilter":False,"filter":{"page":0,"size":1,"query":f"externalincidentid:{sentinel_incident_number}","sort":[{"field":"id","asc":False}],"period":{"by":"day","fromValue":30}}}
    headers = {"content-type": "application/json", "Authorization": f"{XSOAR_API_KEY}"}

    response = requests.post(incident_uri, data=json.dumps(incident_search_body), headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to retrieve XSOAR incident: {response.status_code} - {response.text}")

def get_xsoar_incident_investigation_details(sentinel_incident_number: int):
    """ Retrieve the investigation details the Microsoft Sentinel incident from Cortex XSOAR with a Microsoft Sentinel incident number. """
    response = get_xsoar_incident(sentinel_incident_number)

    data = response.get('data')
    if isinstance(data, list) and len(data) > 0:
        incident = data[0]
    
        return incident.get('CustomFields', {}).get('extendeddetails')