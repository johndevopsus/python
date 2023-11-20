import requests
from requests.auth import HTTPBasicAuth

# Replace these values with your Azure DevOps organization, project, and personal access token
organization = 'YourOrganization'
project = 'YourProject'
pat = 'YourPersonalAccessToken'

# Function to create a new PBI
def create_pbi(title, description, assigned_to):
    url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/$Product%20Backlog%20Item?api-version=7.1'
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {pat}'
    }

    data = {
        'fields': {
            'System.Title': title,
            'System.Description': description,
            'System.AssignedTo': assigned_to
        }
    }

    response = requests.post(url, json=data, headers=headers, auth=HTTPBasicAuth('', pat))

    if response.status_code == 200:
        print(f'PBI created successfully: {response.json()["id"]}')
    else:
        print(f'Failed to create PBI. Status code: {response.status_code}, Error: {response.text}')

# Check if a PBI with a given title already exists and is in "Done" state
def pbi_exists_and_done(title):
    url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/wiql?api-version=7.1'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {pat}'
    }

    query = {
        'query': f"SELECT [System.Id] FROM workitems WHERE [System.Title] = '{title}' AND [System.State] = 'Done'"
    }

    response = requests.post(url, json=query, headers=headers, auth=HTTPBasicAuth('', pat))

    if response.status_code == 200:
        result = response.json()
        return len(result['workItems']) > 0
    else:
        print(f'Error checking PBI status. Status code: {response.status_code}, Error: {response.text}')
        return False

# Example usage
pbi_title = 'Your PBI Title'
pbi_description = 'Your PBI Description'
assigned_user = 'AssignedUser@YourOrganization.com'

if not pbi_exists_and_done(pbi_title):
    create_pbi(pbi_title, pbi_description, assigned_user)
else:
    print(f'A PBI with the title "{pbi_title}" already exists and is in "Done" state.')
