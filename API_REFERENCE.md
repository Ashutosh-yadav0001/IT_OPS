# API Operations Reference

This document provides a quick reference for all available operations in the Graph API client.

## Table of Contents
- [Authentication](#authentication)
- [User Management](#user-management)
- [Group Management](#group-management)
- [Application Management](#application-management)
- [Organization](#organization)
- [Generic Operations](#generic-operations)

## Authentication

### AzureGraphAuth

```python
from azure_auth import AzureGraphAuth

# Initialize with config file
auth = AzureGraphAuth(config_path="config.json")

# Authenticate using client credentials
token = auth.authenticate_client_credentials()

# Check authentication status
if auth.is_authenticated():
    print("Authenticated successfully")

# Get current token
current_token = auth.get_token()
```

## User Management

### List Users

```python
# List top 10 users
users = client.list_users(top=10)

# List users with specific properties
users = client.list_users(
    top=20,
    select=["displayName", "userPrincipalName", "mail", "jobTitle"]
)

# Response structure:
# {
#   "value": [
#     {
#       "displayName": "John Doe",
#       "userPrincipalName": "john.doe@domain.com",
#       "mail": "john.doe@domain.com",
#       "jobTitle": "Developer"
#     }
#   ]
# }
```

### Get User

```python
# Get user by UPN
user = client.get_user("user@domain.com")

# Get user by ID
user = client.get_user("user-object-id")

# Get user with specific properties
user = client.get_user(
    "user@domain.com",
    select=["displayName", "department", "jobTitle", "officeLocation"]
)
```

### Create User

```python
# Create a new user
user_data = {
    "accountEnabled": True,
    "displayName": "Jane Smith",
    "mailNickname": "janes",
    "userPrincipalName": "jane.smith@domain.com",
    "passwordProfile": {
        "forceChangePasswordNextSignIn": True,
        "password": "TempPassword123!"
    }
}
new_user = client.create_user(user_data)
```

### Update User

```python
# Update user properties
update_data = {
    "jobTitle": "Senior Developer",
    "department": "Engineering",
    "officeLocation": "Building 1"
}
result = client.update_user("user@domain.com", update_data)
```

### Delete User

```python
# Delete a user
result = client.delete_user("user@domain.com")
```

## Group Management

### List Groups

```python
# List top 10 groups
groups = client.list_groups(top=10)

# List groups with specific properties
groups = client.list_groups(
    top=20,
    select=["displayName", "description", "mail", "groupTypes"]
)

# Response structure:
# {
#   "value": [
#     {
#       "displayName": "Developers",
#       "description": "Development team",
#       "mail": "developers@domain.com",
#       "groupTypes": ["Unified"]
#     }
#   ]
# }
```

### Get Group

```python
# Get group by ID
group = client.get_group("group-object-id")
```

### Create Group

```python
# Create a new security group
group_data = {
    "displayName": "Engineering Team",
    "mailEnabled": False,
    "mailNickname": "engineering",
    "securityEnabled": True,
    "description": "Engineering department group"
}
new_group = client.create_group(group_data)

# Create a Microsoft 365 group
m365_group_data = {
    "displayName": "Project Team",
    "mailEnabled": True,
    "mailNickname": "projectteam",
    "securityEnabled": False,
    "groupTypes": ["Unified"],
    "description": "Project collaboration group"
}
new_group = client.create_group(m365_group_data)
```

### List Group Members

```python
# Get all members of a group
members = client.list_group_members("group-object-id")

# Response structure:
# {
#   "value": [
#     {
#       "displayName": "John Doe",
#       "userPrincipalName": "john.doe@domain.com",
#       "id": "user-object-id"
#     }
#   ]
# }
```

### Add Group Member

```python
# Add a user to a group
result = client.add_group_member(
    group_id="group-object-id",
    user_id="user-object-id"
)
```

## Application Management

### List Applications

```python
# List top 10 applications
apps = client.list_applications(top=10)

# Response structure:
# {
#   "value": [
#     {
#       "displayName": "My App",
#       "appId": "app-client-id",
#       "id": "app-object-id"
#     }
#   ]
# }
```

### Get Application

```python
# Get application by object ID
app = client.get_application("app-object-id")
```

## Organization

### Get Organization Information

```python
# Get organization details
org = client.get_organization()

# Response structure:
# {
#   "value": [
#     {
#       "displayName": "Contoso",
#       "id": "tenant-id",
#       "verifiedDomains": [...]
#     }
#   ]
# }
```

## Generic Operations

For operations not covered by specific methods, use generic HTTP methods:

### GET Request

```python
# Custom GET request
response = client.get("/users", params={
    "$filter": "department eq 'Engineering'",
    "$select": "displayName,userPrincipalName",
    "$top": "20"
})
```

### POST Request

```python
# Custom POST request
data = {
    "displayName": "New Item",
    "description": "Item description"
}
response = client.post("/endpoint", data=data)
```

### PATCH Request

```python
# Custom PATCH request
update_data = {
    "property": "new value"
}
response = client.patch("/endpoint/item-id", data=update_data)
```

### DELETE Request

```python
# Custom DELETE request
response = client.delete("/endpoint/item-id")
```

## Advanced Queries

### Filtering

```python
# Filter users by department
params = {
    "$filter": "department eq 'Engineering'",
    "$select": "displayName,userPrincipalName,department"
}
users = client.get("/users", params=params)

# Filter with multiple conditions
params = {
    "$filter": "department eq 'Engineering' and accountEnabled eq true",
    "$select": "displayName,userPrincipalName"
}
users = client.get("/users", params=params)
```

### Sorting

```python
# Sort users by display name
params = {
    "$orderby": "displayName",
    "$select": "displayName,userPrincipalName"
}
users = client.get("/users", params=params)
```

### Pagination

```python
# Get paginated results
params = {
    "$top": "10",
    "$skip": "0"
}
users = client.get("/users", params=params)

# Next page
params = {
    "$top": "10",
    "$skip": "10"
}
users = client.get("/users", params=params)
```

### Search

```python
# Search users (requires $search query)
params = {
    "$search": '"displayName:John"',
    "$select": "displayName,userPrincipalName"
}
headers = {
    "ConsistencyLevel": "eventual"
}
# Note: Search requires special headers
```

## Error Handling

All methods return `None` if the request fails. Check the logs for error details:

```python
import logging
logging.basicConfig(level=logging.INFO)

# Make request
users = client.list_users(top=10)

if users:
    print("Success!")
    for user in users['value']:
        print(user['displayName'])
else:
    print("Request failed - check logs")
```

## Common OData Query Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `$select` | Choose properties to return | `$select=displayName,mail` |
| `$filter` | Filter results | `$filter=department eq 'Sales'` |
| `$orderby` | Sort results | `$orderby=displayName` |
| `$top` | Limit results | `$top=10` |
| `$skip` | Skip results (pagination) | `$skip=20` |
| `$expand` | Include related objects | `$expand=manager` |
| `$count` | Include count of results | `$count=true` |
| `$search` | Search across properties | `$search="displayName:John"` |

## Best Practices

1. **Use $select**: Only request properties you need
   ```python
   users = client.list_users(select=["displayName", "mail"])
   ```

2. **Handle pagination**: Use $top and $skip for large result sets
   ```python
   users = client.list_users(top=100)
   ```

3. **Check for None**: Always check if response is None
   ```python
   result = client.get_user(user_id)
   if result:
       # Process result
   else:
       # Handle error
   ```

4. **Enable logging**: Use logging to debug issues
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

5. **Catch exceptions**: Wrap calls in try-except
   ```python
   try:
       users = client.list_users()
   except Exception as e:
       logger.error(f"Error: {e}")
   ```

## Resources

- [Microsoft Graph REST API Reference](https://docs.microsoft.com/en-us/graph/api/overview)
- [OData Query Parameters](https://docs.microsoft.com/en-us/graph/query-parameters)
- [Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer)
