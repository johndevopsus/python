To achieve this, you'll need to modify the script to iterate through each row in your CSV file and either create a new PBI or append tasks to an existing PBI based on your conditions. Here's an example script using the Azure DevOps REST API:

```python
import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

# Replace these values with your Azure DevOps organization, project, and personal access token
organization = 'YourOrganization'
project = 'YourProject'
pat = 'YourPersonalAccessToken'
pbi_title = 'Your PBI Title'
assigned_user = 'AssignedUser@YourOrganization.com'

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
        return response.json()["id"]
    else:
        print(f'Failed to create PBI. Status code: {response.status_code}, Error: {response.text}')
        return None

# Function to add a task to an existing PBI
def add_task_to_pbi(pbi_id, title, description, assigned_to):
    url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{pbi_id}/tasks?api-version=7.1'
    
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
        print(f'Task added successfully to PBI {pbi_id}: {response.json()["id"]}')
    else:
        print(f'Failed to add task to PBI {pbi_id}. Status code: {response.status_code}, Error: {response.text}')

# Read your CSV file into a pandas DataFrame
csv_file_path = 'your_input_file.csv'
df = pd.read_csv(csv_file_path)

# Check if a PBI with the specified title already exists and is in "Done" state
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

# Iterate through each row in the DataFrame and create or update PBIs
for index, row in df.iterrows():
    task_title = row['TaskTitleColumn']
    task_description = row['TaskDescriptionColumn']

    if not pbi_exists_and_done(pbi_title):
        # Create a new PBI
        pbi_id = create_pbi(pbi_title, "PBI Description", assigned_user)
        if pbi_id:
            # Add task to the newly created PBI
            add_task_to_pbi(pbi_id, task_title, task_description, assigned_user)
    else:
        # PBI exists and is in "Done" state, create a new PBI
        pbi_id = create_pbi(pbi_title, "PBI Description", assigned_user)
        if pbi_id:
            # Add task to the newly created PBI
            add_task_to_pbi(pbi_id, task_title, task_description, assigned_user)
```

Make sure to replace 'YourOrganization', 'YourProject', 'YourPersonalAccessToken', 'your_input_file.csv', 'Your PBI Title', 'TaskTitleColumn', and 'TaskDescriptionColumn' with your actual values. Also, adjust the column names in the `iterrows()` loop based on your CSV file structure.

This script iterates through each row in your CSV file, checks if a PBI with the specified title already exists and is in the "Done" state, and either creates a new PBI and adds a task or adds a task to an existing PBI. Adjust it according to your specific requirements and CSV file structure.
