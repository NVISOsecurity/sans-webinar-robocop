import requests
import json
import uuid

from utils.constants import *

def get_access_token(resource: str):
    """
    Fetches an OAuth2 access token using the client credentials flow.
    """
    if resource == SENTINEL_RESOURCE:
        global SENTINEL_ACCESS_TOKEN
        if SENTINEL_ACCESS_TOKEN is None:
            payload = {
                "grant_type": "client_credentials",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "resource": SENTINEL_RESOURCE
            }
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            
            response = requests.post(TOKEN_URL, data=payload, headers=headers)
            response_data = response.json()

            if "access_token" in response_data:
                SENTINEL_ACCESS_TOKEN = response_data["access_token"]
                return SENTINEL_ACCESS_TOKEN
            else:
                raise Exception(f"Failed to retrieve access token: {response_data}")
        else:
            return SENTINEL_ACCESS_TOKEN
    elif resource == LAW_RESOURCE:
        global LAW_ACCESS_TOKEN
        if LAW_ACCESS_TOKEN is None:
            payload = {
                "grant_type": "client_credentials",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "resource": LAW_RESOURCE
            }
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            
            response = requests.post(TOKEN_URL, data=payload, headers=headers)
            response_data = response.json()

            if "access_token" in response_data:
                LAW_ACCESS_TOKEN = response_data["access_token"]
                return LAW_ACCESS_TOKEN
            else:
                raise Exception(f"Failed to retrieve access token: {response_data}")
        else:
            return LAW_ACCESS_TOKEN
    elif resource == ADVANCED_HUNTING_RESOURCE:
        global ADVANCED_HUNTING_ACCESS_TOKEN
        if ADVANCED_HUNTING_ACCESS_TOKEN is None:
            payload = {
                "grant_type": "client_credentials",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "resource": ADVANCED_HUNTING_RESOURCE
            }
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            
            response = requests.post(TOKEN_URL, data=payload, headers=headers)
            response_data = response.json()

            if "access_token" in response_data:
                ADVANCED_HUNTING_ACCESS_TOKEN = response_data["access_token"]
                return ADVANCED_HUNTING_ACCESS_TOKEN
            else:
                raise Exception(f"Failed to retrieve access token: {response_data}")
        else:
            return ADVANCED_HUNTING_ACCESS_TOKEN
        
def get_incident_by_incident_number(incident_number: int):
    """
    Fetches an incident by incident number from Microsoft Sentinel.
    """

    url = f"{SENTINEL_BASE_URL}incidents?api-version={SENTINEL_API_VERSION}&$filter=properties/incidentNumber eq {incident_number}"

    headers = {
        "Authorization": f"Bearer {get_access_token(SENTINEL_RESOURCE)}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to retrieve incident: {response.status_code} - {response.text}")

def get_human_readable_incident_by_id(incident_id: str):
    """
    Fetches an incident by incident ID from Microsoft Sentinel and return human readable output.
    """

    url = f"{SENTINEL_BASE_URL}incidents/{incident_id}?api-version={SENTINEL_API_VERSION}"

    headers = {
        "Authorization": f"Bearer {get_access_token(SENTINEL_RESOURCE)}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        incident = response.json()

        data = "The following details are available for the Microsoft Sentinel incident:\n\n"
        data += "Incident ID: " + incident.get('name', 'N/A') + "\n"
        data += "Incident Number: " + str(incident.get('properties', {}).get('incidentNumber', 'N/A')) + "\n"
        data += "Title: " + incident.get('properties', {}).get('title', 'N/A') + "\n"
        data += "Severity: " + incident.get('properties', {}).get('severity', 'N/A') + "\n"
        data += "Provider: " + incident.get('properties', {}).get('providerName', 'N/A') + "\n"
        data += "Product: " + ','.join(incident.get('properties', {}).get('additionalData', {}).get('alertProductNames', [])) + "\n"
        data += "Tactics: " + ','.join(incident.get('properties', {}).get('additionalData', {}).get('tactics', [])) + "\n"
        data += "Techniques: " + ','.join(incident.get('properties', {}).get('additionalData', {}).get('techniques', [])) + "\n"
        data += "Created Time: " + incident.get('properties', {}).get('createdTimeUtc', 'N/A') + "\n"
        data += "Modified Time: " + incident.get('properties', {}).get('lastModifiedTimeUtc', 'N/A') + "\n"

        return data
    else:
        raise Exception(f"Failed to retrieve incident: {response.status_code} - {response.text}")
    
def get_incident_by_id(incident_id: str):
    """
    Fetches an incident by incident ID from Microsoft Sentinel.
    """

    url = f"{SENTINEL_BASE_URL}incidents/{incident_id}?api-version={SENTINEL_API_VERSION}"

    headers = {
        "Authorization": f"Bearer {get_access_token(SENTINEL_RESOURCE)}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        incident = response.json()
        # Remove specific fields
        if 'properties' in incident:
            incident['properties'].pop('status', None)
            incident['properties'].pop('classification', None)
            incident['properties'].pop('classificationComment', None)
            incident['properties'].pop('classificationReason', None)
        return incident
    else:
        raise Exception(f"Failed to retrieve incident: {response.status_code} - {response.text}")
      
def get_human_readable_incident_alerts(incident_id: str):
    """
    Fetches alerts associated with an incident from Microsoft Sentinel and return human readable output.
    """

    url = f"{SENTINEL_BASE_URL}incidents/{incident_id}/alerts?api-version={SENTINEL_API_VERSION}"

    headers = {
        "Authorization": f"Bearer {get_access_token(SENTINEL_RESOURCE)}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        data = "The following alerts are associated with the Microsoft Sentinel incident:\n\n"
        for alert in response.json().get('value', []):
            techniques = alert.get('properties', {}).get('additionalData', {}).get('MitreTechniques', [])
            try:
                MitreTechniques = json.loads(techniques)
            except:
                MitreTechniques = techniques
            data += "Alert ID: " + alert.get('name', 'N/A') + "\n"
            data += "Title: " + alert.get('properties', {}).get('alertDisplayName', 'N/A') + "\n"
            data += "Severity: " + alert.get('properties', {}).get('severity', 'N/A') + "\n"
            data += "Vendor: " + alert.get('properties', {}).get('vendorName', 'N/A') + "\n"
            data += "Product: " + alert.get('properties', {}).get('productName', 'N/A') + "\n"
            data += "Component: " + alert.get('properties', {}).get('productComponentName', 'N/A') + "\n"
            data += "Confidence Level: " + alert.get('properties', {}).get('confidenceLevel', 'N/A') + "\n"
            data += "Tactics: " + ','.join(alert.get('properties', {}).get('tactics', [])) + "\n"
            data += "Techniques: " + ','.join(MitreTechniques) + "\n"
            data += "Time Generated: " + alert.get('properties', {}).get('timeGenerated', 'N/A') + "\n"
            data += "Description: " + alert.get('properties', {}).get('description', 'N/A') + "\n\n"
            

        return data
    else:
        raise Exception(f"Failed to retrieve incident alerts: {response.status_code} - {response.text}")
    
def get_incident_alerts(incident_id: str):
    """
    Fetches alerts associated with an incident from Microsoft Sentinel and return human readable output.
    """

    url = f"{SENTINEL_BASE_URL}incidents/{incident_id}/alerts?api-version={SENTINEL_API_VERSION}"

    headers = {
        "Authorization": f"Bearer {get_access_token(SENTINEL_RESOURCE)}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to retrieve incident alerts: {response.status_code} - {response.text}")
    
def get_incident_entities(incident_id: str):
    """
    Fetches entities associated with an incident from Microsoft Sentinel.
    """

    url = f"{SENTINEL_BASE_URL}incidents/{incident_id}/entities?api-version={SENTINEL_API_VERSION}"

    headers = {
        "Authorization": f"Bearer {get_access_token(SENTINEL_RESOURCE)}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to retrieve incident entities: {response.status_code} - {response.text}")
    
def get_human_readable_incident_entities(incident_id: str):
    """
    Fetches entities associated with an incident from Microsoft Sentinel.
    """

    url = f"{SENTINEL_BASE_URL}incidents/{incident_id}/entities?api-version={SENTINEL_API_VERSION}"

    headers = {
        "Authorization": f"Bearer {get_access_token(SENTINEL_RESOURCE)}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        # return response.json()
        data = "The following entities with their properties are associated with the Microsoft Sentinel incident:\n\n"
        for entity in response.json()['entities']:
            data += "Type: " + entity['kind']+ ":\n"
            for k,v in entity['properties'].items():
                data += f"{k}: {v}\n"
            data += "\n"
        return data
    else:
        raise Exception(f"Failed to retrieve incident entities: {response.status_code} - {response.text}")

def query_sentinel_log_analytics_workspace(query: str):
    """
    Queries a Microsoft Sentinel Log Analytics workspace.
    """

    url = f"https://api.loganalytics.io/v1/workspaces/{WORKSPACE_ID}/query"
    
    headers = {
        "Authorization": f"Bearer {get_access_token(LAW_RESOURCE)}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers, params={"query": query})

    if response.status_code == 200:
        result = response.json()
    else:
        raise Exception(f"Failed to execute query: {response.status_code} - {response.text}")

    results_rows = 0

    output = []
    for table in result["tables"]:
        for row in table["rows"]:
            results_rows += 1
            return_row = {}
            for column in range(len(table["columns"])):
                if table["columns"][column]["type"] == "dynamic":
                    try:
                        return_row[table["columns"][column]["name"]] = json.loads(row[column])
                    except:
                        return_row[table["columns"][column]["name"]] = row[column]
                else:
                    return_row[table["columns"][column]["name"]] = row[column]
            return_row.update({"uuid": str(uuid.uuid4())})
            output.append(return_row)

    return output

def query_defender_advanced_hunting(query: str):
    """
    Queries Microsoft Defender Advanced Hunting.
    """

    url = f"https://api.security.microsoft.com/api/advancedhunting/run"
    
    headers = {
        "Authorization": f"Bearer {get_access_token(ADVANCED_HUNTING_RESOURCE)}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, data=json.dumps({"Query": query}))

    if response.status_code == 200:
        return response.json().get('Results', [])
    else:
        raise Exception(f"Failed to execute query: {response.status_code} - {response.text}")

def get_sentinel_tables():
    """
    Fetches the tables with data larger than 1MB available in the Microsoft Sentinel Log Analytics workspace with their columns and field types.
    """

    data = {}

    url = f'https://management.azure.com/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{RESOURCE_GROUP}/providers/Microsoft.OperationalInsights/workspaces/{WORKSPACE_NAME}/tables?api-version=2023-09-01'
    
    headers = {
        "Authorization": f"Bearer {get_access_token(SENTINEL_RESOURCE)}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        tables = response.json().get('value', [])
        for table in tables:
            table_schema = table.get('properties', {}).get('schema', {})
            table_name = table_schema.get('name')
            table_columns = [column.get('name')+ ': ' + column.get('type') for column in table_schema.get('standardColumns', [])]
            data[table_name] = table_columns
        

        query = "Usage | where StartTime > ago(30d) | summarize ['Table Size'] =sum(Quantity) by ['Table Name'] =DataType, ['IsBillable'] =IsBillable | where ['Table Size'] >1"
        result = query_sentinel_log_analytics_workspace(query=query)

        filtered_data = {}

        for table in result:
            table_name = table.get('Table Name')
            if table_name in data.keys():
                filtered_data[table_name] = data.get(table_name)

        tables_and_columns = "The following tables with their collumn names and field types are available in the Microsoft Sentinel and can be used in KQL queries:\n"
    
        for table, columns in filtered_data.items():
            tables_and_columns += f"{table}:\n"
            for column in columns:
                tables_and_columns += f"- {column}\n"

        return tables_and_columns

    else:
        raise Exception(f"Failed to retrieve tables: {response.status_code} - {response.text}")
