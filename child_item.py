import requests
from requests.auth import HTTPBasicAuth

# Replace these values with your Azure DevOps organization, project, and personal access token
organization = "YourOrganization"
project = "YourProject"
personal_access_token = "YourPersonalAccessToken"
work_item_id = "YourWorkItemID"

# Azure DevOps REST API base URL
base_url = f"https://dev.azure.com/{organization}/{project}/_apis"

# REST API endpoint to get work item details
url = f"{base_url}/wit/workitems/{work_item_id}"

# Define request headers with authorization
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {personal_access_token}"
}

# Make the request to get work item details
response = requests.get(url, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    work_item_data = response.json()

    # Extract child items
    if "relations" in work_item_data:
        child_items = [relation["url"] for relation in work_item_data["relations"] if relation["rel"] == "System.LinkTypes.Hierarchy-Reverse"]

        # Retrieve details for each child item
        for child_url in child_items:
            child_response = requests.get(child_url, headers=headers)
            
            if child_response.status_code == 200:
                child_data = child_response.json()
                title = child_data["fields"].get("System.Title", "")
                state = child_data["fields"].get("System.State", "")
                
                # Print the results
                print(f"Child Item Title: {title}, State: {state}")
            else:
                print(f"Error retrieving child item details: {child_response.status_code} - {child_response.text}")
    else:
        print("No child items found for the specified work item.")
else:
    # Print an error message if the request was not successful
    print(f"Error: {response.status_code} - {response.text}")



############################################################
#to fetch the work item details, iterate through its child items, filter out tasks that are not in the "Done" state, and then compare the resulting list with your provided list

import requests
from requests.auth import HTTPBasicAuth

# Replace these values with your Azure DevOps organization, project, and personal access token
organization = "YourOrganization"
project = "YourProject"
personal_access_token = "YourPersonalAccessToken"
parent_work_item_id = "YourParentWorkItemID"
your_list_of_tasks = ["Task1", "Task2", "Task3"]  # Replace with your actual list

# Azure DevOps REST API base URL
base_url = f"https://dev.azure.com/{organization}/{project}/_apis"

# Get work item details
def get_work_item_details(work_item_id):
    url = f"{base_url}/wit/workitems/{work_item_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {personal_access_token}"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

# Get child items with type 'task' and state not 'Done'
def get_non_done_tasks(work_item_data):
    tasks = []
    for child in work_item_data.get("relations", []):
        if (
            child.get("rel", "").lower() == "system.linktypes.hierarchy-reverse"
            and child.get("attributes", {}).get("name", "").lower() == "child"
        ):
            child_id = child.get("url", "").split("/")[-1]
            child_details = get_work_item_details(child_id)
            child_type = child_details["fields"].get("System.WorkItemType", "").lower()
            child_state = child_details["fields"].get("System.State", "").lower()
            child_title = child_details["fields"].get("System.Title", "")
            if child_type == "task" and child_state != "done":
                tasks.append(child_title)
    return tasks

# Compare with your list and print the differences
def compare_lists(api_tasks, your_list):
    api_set = set(api_tasks)
    your_set = set(your_list)
    differences = api_set.symmetric_difference(your_set)

    print("Tasks in API but not in your list:")
    print("\n".join(differences.intersection(api_set)))

    print("\nTasks in your list but not in API:")
    print("\n".join(differences.intersection(your_set)))

# Main script
try:
    parent_work_item_data = get_work_item_details(parent_work_item_id)
    api_tasks = get_non_done_tasks(parent_work_item_data)
    compare_lists(api_tasks, your_list_of_tasks)
except Exception as e:
    print(f"An error occurred: {e}")
