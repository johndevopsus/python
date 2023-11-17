import requests
from requests.auth import HTTPBasicAuth

# Azure DevOps organization URL and project name
organization_url = 'https://dev.azure.com/YourOrganization'
project_name = 'YourProject'

# Personal Access Token (PAT) for authentication
pat = 'your_personal_access_token'

# Base URL for Azure DevOps REST API
base_url = f'{organization_url}/{project_name}/_apis/'

# Function to create a new PBI
def create_pbi(title, description):
    url = base_url + 'wit/workitems/$Product Backlog Item?api-version=6.0'
    
    # PBI payload
    payload = [
        {
            "op": "add",
            "path": "/fields/System.Title",
            "value": title
        },
        {
            "op": "add",
            "path": "/fields/System.Description",
            "value": description
        }
    ]
    
    response = requests.post(url, json=payload, auth=HTTPBasicAuth('', pat))
    
    if response.status_code == 200:
        return response.json()['id']
    else:
        print(f"Failed to create PBI. Status code: {response.status_code}")
        return None

# Function to create a task and assign it to a user
def create_task(pbi_id, title, assigned_to):
    url = base_url + 'wit/workitems/$Task?api-version=6.0'
    
    # Task payload
    payload = [
        {
            "op": "add",
            "path": "/fields/System.Title",
            "value": title
        },
        {
            "op": "add",
            "path": "/fields/System.AssignedTo",
            "value": assigned_to
        },
        {
            "op": "add",
            "path": "/relations/-",
            "value": {
                "rel": "System.LinkTypes.Hierarchy-Reverse",
                "url": f"{base_url}wit/workitems/{pbi_id}"
            }
        }
    ]
    
    response = requests.post(url, json=payload, auth=HTTPBasicAuth('', pat))
    
    if response.status_code != 200:
        print(f"Failed to create task. Status code: {response.status_code}")

# Example usage
pbi_title = 'New Feature'
pbi_description = 'Implement a new feature in the application.'

# Create a new PBI
pbi_id = create_pbi(pbi_title, pbi_description)

if pbi_id is not None:
    # Create tasks and assign them
    tasks = [
        {"title": "Task 1", "assigned_to": "user1@yourdomain.com"},
        {"title": "Task 2", "assigned_to": "user2@yourdomain.com"}
    ]
    
    for task in tasks:
        create_task(pbi_id, task['title'], task['assigned_to'])

# Please replace placeholders like 'YourOrganization', 'YourProject', 'your_personal_access_token', etc., with your actual Azure DevOps organization, project, and personal access token information. Make sure that the user specified in the task assignment exists in your Azure DevOps project.
#This script uses the Azure DevOps REST API version 6.0. Depending on the version you're using, you might need to adjust the API version in the URLs. Additionally, consider handling errors and exceptions more gracefully in a production setting.
