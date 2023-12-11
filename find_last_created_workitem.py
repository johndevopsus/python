import requests
from requests.auth import HTTPBasicAuth

def find_last_created_workitem(organization, project, pat, title):
    url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/wiql?api-version=7.1'

    # WIQL (Work Item Query Language) to find work items with a specific title
    wiql_query = f"""
    SELECT [System.Id], [System.State] FROM WorkItems
    WHERE [System.Title] = '{title}'
    ORDER BY [System.CreatedDate] DESC
    """

    
    headers = {
        'Content-Type': 'application/json',
    }

    # Prepare the request payload
    data = {
        'query': wiql_query
    }

    # Make the request to get the work item IDs
    response = requests.post(url, headers=headers, auth=HTTPBasicAuth('', pat), json=data)

    if response.status_code == 200:
        result = response.json()

        # Check if any work items were found
        if 'workItems' in result and len(result['workItems']) > 0:
            # Get the ID of the last created work item
            last_created_item_id = result['workItems'][0]['id']

            # Call another API to get the details of the work item, including its state
            workitem_url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{last_created_item_id}?api-version=7.1'
            workitem_response = requests.get(workitem_url, headers=headers, auth=HTTPBasicAuth('', pat))

            if workitem_response.status_code == 200:
                workitem_data = workitem_response.json()
                item_state = workitem_data['fields']['System.State']

                if item_state == 'Done':
                    print(f"Item ID {last_created_item_id} is closed.")
                else:
                    print(f"Item ID {last_created_item_id} is not closed. State: {item_state}")

            else:
                print(f"Failed to retrieve details for work item {last_created_item_id}. Status code: {workitem_response.status_code}")
                print(workitem_response.text)
        else:
            print(f"No work items found with title '{title}'")
    else:
        print(f"Failed to query work items. Status code: {response.status_code}")
        print(response.text)

# Replace these variables with your own values
organization = 'YourOrganization'
project = 'YourProject'
pat = 'YourPersonalAccessToken'
work_item_title = 'YourWorkItemTitle'  # Replace with the title you want to search

# Call the function to find the last created work item and check its status
find_last_created_workitem(organization, project, pat, work_item_title)
