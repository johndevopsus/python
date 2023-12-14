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

#Python script to get each "Child Item" type is task, title is any, and state status is not "Done" from a specific "workitem" in Azure DevOps Board. I need it as a python list.


import requests
from requests.auth import HTTPBasicAuth

def get_child_items(work_item_id, organization, project, personal_access_token):
    # Azure DevOps REST API base URL
    base_url = f"https://dev.azure.com/{organization}/{project}/_apis"

    # REST API endpoint to get work item details including child items
    url = f"{base_url}/wit/workitems/{work_item_id}?expand=children"

    # Define request headers with authorization
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {personal_access_token}"
    }

    # Make the request to get work item details including child items
    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        work_item_data = response.json()

        # Extract child items
        child_items = work_item_data.get("relations", [])

        # Create a list to store child item details
        child_items_list = []

        # Iterate through child items and extract information
        for item in child_items:
            if "attributes" in item and "child" in item["attributes"]:
                child_item_id = item["attributes"]["child"]["id"]
                
                # Get details of the child item
                child_item_details = get_work_item_details(child_item_id, organization, project, personal_access_token)

                # Append child item details to the list
                child_items_list.append(child_item_details)

        return child_items_list
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code} - {response.text}")
        return None

def get_work_item_details(work_item_id, organization, project, personal_access_token):
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

        # Extract work item type, title, and status
        item_type = work_item_data["fields"].get("System.WorkItemType", "")
        title = work_item_data["fields"].get("System.Title", "")
        status = work_item_data["fields"].get("System.State", "")

        # Return a dictionary with work item details
        return {
            "Type": item_type,
            "Title": title,
            "Status": status
        }
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Replace these values with your Azure DevOps organization, project, and personal access token
organization = "YourOrganization"
project = "YourProject"
personal_access_token = "YourPersonalAccessToken"
work_item_id = "YourWorkItemID"

# Get child items details for a specific work item
child_items_list = get_child_items(work_item_id, organization, project, personal_access_token)

# Print the list of child items
if child_items_list:
    for child_item in child_items_list:
        print(child_item)



################################################################################################

import requests
from requests.auth import HTTPBasicAuth

def get_child_tasks(work_item_id, personal_access_token):
    # Replace these values with your Azure DevOps organization, project, and personal access token
    organization = "YourOrganization"
    project = "YourProject"

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

        # Extract child items of type "Task" with state not equal to "Done"
        child_tasks = []
        for relation in work_item_data.get("relations", []):
            if "attributes" in relation and relation["attributes"].get("name") == "Child":
                child_item_id = relation.get("target", {}).get("id")
                child_state = work_item_data.get("fields", {}).get(f"{child_item_id}.System.State", "")
                child_type = work_item_data.get("fields", {}).get(f"{child_item_id}.System.WorkItemType", "")
                child_title = work_item_data.get("fields", {}).get(f"{child_item_id}.System.Title", "")

                # Check if the child item is of type "Task" and state is not "Done"
                if child_type == "Task" and child_state != "Done":
                    child_tasks.append({"Task": child_title, "State": child_state})

        return child_tasks
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code} - {response.text}")
        return []

# Replace the placeholder values for personal_access_token and work_item_id
personal_access_token = "YourPersonalAccessToken"
work_item_id = "YourWorkItemID"

# Get child tasks that meet the specified criteria
result = get_child_tasks(work_item_id, personal_access_token)

# Print the result
print(result)



#+++++++++++++++++++++++++++#

import requests
from requests.auth import HTTPBasicAuth

# Replace these values with your Azure DevOps organization, project, personal access token, and work item ID
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

    # Extract the title of the first child item (if available)
    child_items = work_item_data.get("relations", [])
    if child_items:
        first_child_item_title = work_item_data["fields"].get(f"{child_items[0]['target']['id']}.System.Title", "")
        print(f"Title of the first child item: {first_child_item_title}")
    else:
        print("No child items found.")
else:
    # Print an error message if the request was not successful
    print(f"Error: {response.status_code} - {response.text}")




#@@@@@@@@@@@@@@@@@@@#

import requests
from requests.auth import HTTPBasicAuth

# Replace these values with your Azure DevOps organization, project, personal access token, and PBI item ID
organization = "YourOrganization"
project = "YourProject"
personal_access_token = "YourPersonalAccessToken"
pbi_item_id = "YourPBIItemID"

# Azure DevOps REST API base URL
base_url = f"https://dev.azure.com/{organization}/{project}/_apis"

# REST API endpoint to get PBI item details
url = f"{base_url}/wit/workitems/{pbi_item_id}"

# Define request headers with authorization
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {personal_access_token}"
}

# Make the request to get PBI item details
response = requests.get(url, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    pbi_item_data = response.json()

    # Extract child items (tasks) IDs
    child_item_ids = []

    for relation in pbi_item_data.get("relations", []):
        if relation.get("attributes", {}).get("name") == "Child":
            child_item_id = relation.get("target", {}).get("id")
            child_item_ids.append(child_item_id)

    if child_item_ids:
        print(f"Child Item IDs: {child_item_ids}")
    else:
        print("No child items found.")
else:
    # Print an error message if the request was not successful
    print(f"Error: {response.status_code} - {response.text}")




