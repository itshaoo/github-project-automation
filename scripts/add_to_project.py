import os
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
PROJECT_ID = os.getenv("PROJECT_ID")
ISSUE_ID = os.getenv("ISSUE_ID")

url = "https://api.github.com/graphql"

query = """
mutation($projectId: ID!, $contentId: ID!) {
  addProjectV2ItemById(input: {
    projectId: $projectId,
    contentId: $contentId
  }) {
    item {
      id
    }
  }
}
"""

variables = {
    "projectId": PROJECT_ID,
    "contentId": ISSUE_ID
}

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}"
}

labels = os.getenv("LABELS", "")
label_list = labels.split(",")

print("Labels:", label_list)

if "bug" in label_list:
    print("Set Type = Bug")
elif "feature" in label_list:
    print("Set Type = Feature")
else:
    print("No matching label")

response = requests.post(url, json={"query": query, "variables": variables}, headers=headers)

print(response.json())
