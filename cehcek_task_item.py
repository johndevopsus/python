import requests
from requests.auth import HTTPBasicAuth

# Replace these variables with your own values
organization = 'YourOrganization'
project = 'YourProject'
pat = 'YourPersonalAccessToken'
work_item_id = '123'  # Replace with the ID of the work item you want to check
task_title_to_check = 'YourTaskTitle'  # Replace with the title of the task you want to check

url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{work_item_id}?api-version=7.1'

headers = {
    'Content-Type': 'application/json',
}

response = requests.get(url, headers=headers, auth=HTTPBasicAuth('', pat))

if response.status_code == 200:
    work_item_data = response.json()

    # Check if the work item has tasks
    if 'fields' in work_item_data and 'System.Tasks' in work_item_data['fields']:
        tasks = work_item_data['fields']['System.Tasks']

        # Check if there is an unchecked task with the specified title
        unchecked_task_found = any(
            task['fields']['System.State'] != 'Closed' and
            task['fields']['System.Title'] == task_title_to_check
            for task in tasks
        )

        if unchecked_task_found:
            print(f"Unchecked task with title '{task_title_to_check}' found in work item {work_item_id}")
        else:
            print(f"No unchecked task with title '{task_title_to_check}' found in work item {work_item_id}")

    else:
        print(f"Work item {work_item_id} has no tasks.")
else:
    print(f"Failed to retrieve work item {work_item_id}. Status code: {response.status_code}")
    print(response.text)
