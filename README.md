# IT_OPS - Azure Graph API Integration

A Python-based implementation for working with Microsoft Graph API to manage Azure Active Directory resources including users, groups, applications, and more.

## Overview

This project provides a clean and simple interface to interact with Microsoft Graph API, making it easy to:
- Authenticate with Azure AD using client credentials
- Manage users and groups
- Query organization information
- Perform custom Graph API operations
- Handle common Azure AD administrative tasks

## Features

- **Simple Authentication**: Easy-to-use authentication with Azure AD using MSAL
- **Comprehensive Client**: Full-featured Graph API client with common operations
- **Type-Safe**: Well-documented methods with clear parameter types
- **Error Handling**: Robust error handling and logging
- **Examples**: Multiple example scripts demonstrating various use cases
- **Extensible**: Easy to extend with custom Graph API operations

## Prerequisites

- Python 3.7 or higher
- Azure AD tenant
- Azure AD application registration with appropriate permissions
- Client credentials (Client ID, Tenant ID, Client Secret)

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Ashutosh-yadav0001/IT_OPS.git
cd IT_OPS
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Azure AD Application

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** > **App registrations**
3. Click **New registration**
4. Provide a name for your application
5. Set **Supported account types** (typically single tenant)
6. Click **Register**

After registration:

7. Note the **Application (client) ID** and **Directory (tenant) ID**
8. Go to **Certificates & secrets**
9. Create a **New client secret** and note the value
10. Go to **API permissions**
11. Add the following Microsoft Graph **Application permissions**:
    - `User.Read.All` - Read all users' full profiles
    - `Group.Read.All` - Read all groups
    - `Application.Read.All` - Read all applications (optional)
    - `Organization.Read.All` - Read organization information (optional)
12. Click **Grant admin consent** for your tenant

### 4. Configure the Application

1. Copy the configuration template:
   ```bash
   cp config.template.json config.json
   ```

2. Edit `config.json` and fill in your credentials:
   ```json
   {
     "azure": {
       "tenant_id": "your-tenant-id-here",
       "client_id": "your-client-id-here",
       "client_secret": "your-client-secret-here",
       "authority": "https://login.microsoftonline.com/your-tenant-id-here",
       "scope": ["https://graph.microsoft.com/.default"]
     }
   }
   ```

   **Note**: Never commit `config.json` to version control. It's already in `.gitignore`.

## Usage

### Basic Example

Run the basic example to list users and groups:

```bash
python example_basic.py
```

This script demonstrates:
- Authentication with Azure AD
- Listing users
- Listing groups
- Getting organization information

### Advanced Example

Run the advanced example for more complex operations:

```bash
python example_advanced.py
```

This script demonstrates:
- User management operations
- Group management and membership
- Application listing
- Custom Graph API queries

### Using in Your Code

```python
from azure_auth import AzureGraphAuth
from graph_client import GraphAPIClient

# Authenticate
auth = AzureGraphAuth(config_path="config.json")
auth.authenticate_client_credentials()

# Create client
client = GraphAPIClient(auth)

# List users
users = client.list_users(top=10)
if users and 'value' in users:
    for user in users['value']:
        print(f"User: {user['displayName']}")

# Get specific user
user = client.get_user("user@yourdomain.com")

# List groups
groups = client.list_groups(top=10)

# Custom query
result = client.get("/me")  # Get current app's service principal
```

## Project Structure

```
IT_OPS/
├── azure_auth.py              # Authentication module
├── graph_client.py            # Graph API client
├── example_basic.py           # Basic usage examples
├── example_advanced.py        # Advanced usage examples
├── requirements.txt           # Python dependencies
├── config.template.json       # Configuration template
├── config.json               # Your configuration (not in git)
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## Available Operations

### User Management
- `list_users()` - List all users
- `get_user(user_id)` - Get specific user
- `create_user(user_data)` - Create new user
- `update_user(user_id, user_data)` - Update user
- `delete_user(user_id)` - Delete user

### Group Management
- `list_groups()` - List all groups
- `get_group(group_id)` - Get specific group
- `create_group(group_data)` - Create new group
- `list_group_members(group_id)` - List group members
- `add_group_member(group_id, user_id)` - Add member to group

### Application Management
- `list_applications()` - List registered applications
- `get_application(app_id)` - Get specific application

### Organization
- `get_organization()` - Get organization information

### Generic Operations
- `get(endpoint, params)` - Generic GET request
- `post(endpoint, data)` - Generic POST request
- `patch(endpoint, data)` - Generic PATCH request
- `delete(endpoint)` - Generic DELETE request

## Common Use Cases

### Example 1: Find Users by Department

```python
params = {
    "$filter": "department eq 'Engineering'",
    "$select": "displayName,userPrincipalName,department"
}
users = client.get("/users", params=params)
```

### Example 2: Get Group Members

```python
group_id = "group-object-id"
members = client.list_group_members(group_id)
if members and 'value' in members:
    for member in members['value']:
        print(member['displayName'])
```

### Example 3: Update User Properties

```python
user_id = "user@domain.com"
update_data = {
    "jobTitle": "Senior Engineer",
    "department": "Engineering"
}
result = client.update_user(user_id, update_data)
```

## Troubleshooting

### Authentication Fails

1. Verify your credentials in `config.json`
2. Ensure the client secret hasn't expired
3. Check that admin consent has been granted for API permissions
4. Verify the tenant ID and authority URL are correct

### Permission Denied Errors

1. Check that your application has the required API permissions
2. Ensure admin consent has been granted
3. Verify you're using Application permissions (not Delegated) for client credentials flow

### API Request Fails

1. Check the error message and HTTP status code in logs
2. Verify the endpoint URL is correct
3. Ensure your token hasn't expired (the client handles this automatically)
4. Check Microsoft Graph API documentation for specific endpoint requirements

## Security Best Practices

1. **Never commit credentials**: `config.json` is in `.gitignore` - keep it that way
2. **Rotate secrets regularly**: Change client secrets periodically
3. **Use least privilege**: Only request necessary API permissions
4. **Secure storage**: Store credentials securely (e.g., Azure Key Vault in production)
5. **Monitor access**: Review application sign-in logs regularly

## API Documentation

- [Microsoft Graph REST API Reference](https://docs.microsoft.com/en-us/graph/api/overview)
- [Azure AD App Registration](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)
- [Microsoft Graph Permissions](https://docs.microsoft.com/en-us/graph/permissions-reference)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is provided as-is for educational and operational purposes.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review Microsoft Graph API documentation
3. Open an issue in this repository
