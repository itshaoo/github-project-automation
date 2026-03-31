import os
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
PROJECT_ID = os.getenv("PROJECT_ID")
ISSUE_ID = os.getenv("ISSUE_ID")

# 你的 Type 欄位資訊
FIELD_ID = "PVTSSF_lAHOBWfN6M4BSulnzhAldTI"
BUG_OPTION_ID = "55ecb108"
FEATURE_OPTION_ID = "6591599e"

url = "https://api.github.com/graphql"

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}"
}

# -----------------------------
# Step 1：加入 Project
# -----------------------------
add_query = """
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

response = requests.post(url, json={"query": add_query, "variables": variables}, headers=headers)
data = response.json()

print("Add Item Response:", data)

# ⚠️ 拿 item_id（很重要）
item_id = data["data"]["addProjectV2ItemById"]["item"]["id"]

# -----------------------------
# Step 2：判斷 label → 決定 Type
# -----------------------------
labels = os.getenv("LABELS", "")
label_list = [l.strip().lower() for l in labels.split(",")]

print("Labels:", label_list)

type_value = None

if "bug" in label_list:
    type_value = BUG_OPTION_ID
    print("Set Type = Bug")
elif "feature" in label_list:
    type_value = FEATURE_OPTION_ID
    print("Set Type = Feature")
else:
    print("No matching label")

# -----------------------------
# Step 3：更新 Type 欄位
# -----------------------------
if type_value:
    update_query = """
    mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
      updateProjectV2ItemFieldValue(input: {
        projectId: $projectId,
        itemId: $itemId,
        fieldId: $fieldId,
        value: {
          singleSelectOptionId: $optionId
        }
      }) {
        projectV2Item {
          id
        }
      }
    }
    """

    variables = {
        "projectId": PROJECT_ID,
        "itemId": item_id,
        "fieldId": FIELD_ID,
        "optionId": type_value
    }

    response = requests.post(url, json={"query": update_query, "variables": variables}, headers=headers)
    print("Update Type Response:", response.json())
